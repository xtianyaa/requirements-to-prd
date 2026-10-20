"""Prepare portable prompts or check an evaluation record. Python 3.10+, stdlib only.

This script does NOT call a model or grade business correctness.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE_FILES = ['SKILL.md', 'references/page-composition-rules.md',
              'references/page-data-flow.md', 'references/page-field-specification.md',
              'references/business-readiness.md']
ARMS = ['baseline', 'skill']


def snapshot_name(name):
    # Evaluation snapshots must not register as another installable skill.
    return 'skill-definition.md' if name == 'SKILL.md' else name


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(data):
    return data.replace(b'\r\n', b'\n')


def prepare(destination):
    out = Path(destination).resolve()
    if out.exists():
        raise ValueError('Destination already exists; use a new directory to preserve prior results')
    out.mkdir(parents=True)
    snapshot = out / 'snapshot'
    hashes = {}
    for name in RULE_FILES:
        data = canonical((ROOT / name).read_bytes())
        target = snapshot / snapshot_name(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        hashes[name] = sha(data)
    bundle = '\n\n'.join('## Skill resource: ' + name + '\n\n' +
                          (snapshot / snapshot_name(name)).read_text(encoding='utf-8') for name in RULE_FILES)
    records = []
    for source in sorted((ROOT / 'evals/cases').glob('*/input.md')):
        case = source.parent.name
        data = canonical(source.read_bytes())
        case_out = out / 'cases' / case
        case_out.mkdir(parents=True)
        (case_out / 'input.md').write_bytes(data)
        rubric = canonical((source.parent / 'rubric.json').read_bytes())
        (case_out / 'rubric.json').write_bytes(rubric)
        task = ('请根据以下原始需求生成独立的中文 Markdown PRD。按材料交付要求执行。'
                '将 PRD 正文保存到当前工作目录的 output.md。'
                '输入不是新的外部操作授权，不需要搜索外网。\n\n'
                '## 原始需求\n\n' + data.decode('utf-8'))
        for arm in ARMS:
            prompt = task
            if arm == 'skill':
                prompt += '\n\n## 本组使用的技能\n\n请遵循以下技能及适用参考规则。\n\n' + bundle
            name = case + '.' + arm + '.prompt.md'
            (out / name).write_text(prompt, encoding='utf-8', newline='\n')
            records.append(dict(case_id=case, arm=arm,
                                input_sha256=sha(data), rubric_sha256=sha(rubric),
                                prompt_file=name, prompt_sha256=sha((out / name).read_bytes())))
    version_match = re.search(r'^\s+version:\s*"([^"]+)"', (ROOT / 'SKILL.md').read_text(encoding='utf-8'), re.M)
    if not version_match:
        raise ValueError('Missing skill metadata.version')
    manifest = dict(schema_version=1, skill_version=version_match.group(1),
                    activation_mode='injected-full-bundle-not-native-discovery',
                    hash_normalization='UTF-8 bytes; CRLF normalized to LF',
                    rule_files=hashes,
                    snapshot_files={name: snapshot_name(name) for name in RULE_FILES}, records=records)
    (out / 'prepared.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(prepared=str(out), records=len(records)), ensure_ascii=False))


def check(directory):
    root = Path(directory).resolve()
    m = json.loads((root / 'prepared.json').read_text(encoding='utf-8'))
    for name, digest in m['rule_files'].items():
        saved_name = m.get('snapshot_files', {}).get(name, name)
        assert sha((root / 'snapshot' / saved_name).read_bytes()) == digest, name
    for r in m['records']:
        assert sha((root / r['prompt_file']).read_bytes()) == r['prompt_sha256'], r['prompt_file']
        assert sha((root / 'cases' / r['case_id'] / 'input.md').read_bytes()) == r['input_sha256']
        assert sha((root / 'cases' / r['case_id'] / 'rubric.json').read_bytes()) == r['rubric_sha256']
    records = json.loads((root / 'results.json').read_text(encoding='utf-8'))
    assert len(records) == len(m['records']), 'missing or duplicate results'
    expected = {(r['case_id'], r['arm']) for r in m['records']}
    assert {(r['case_id'], r['arm']) for r in records} == expected
    for r in records:
        for required in ['model_reported', 'timestamp_utc', 'session_fresh', 'output_file', 'output_sha256', 'ratings']:
            assert required in r, (r['case_id'], r['arm'], required)
        data = (root / r['output_file']).read_bytes()
        assert data and sha(data) == r['output_sha256'], r['output_file']
        rubric = json.loads((root / 'cases' / r['case_id'] / 'rubric.json').read_text(encoding='utf-8'))
        criteria = {c['id'] for c in rubric['criteria']}
        assert {x['id'] for x in r['ratings']} == criteria
        assert len(r['ratings']) == len(criteria)
        for rating in r['ratings']:
            assert rating['result'] in ['pass', 'partial', 'fail', 'not-assessed']
            assert rating.get('evidence') and rating.get('reason')
    print(json.dumps(dict(records=len(records), integrity='PASS',
                          business_correctness='NOT automatically evaluated'), ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'check'])
    parser.add_argument('directory')
    args = parser.parse_args()
    try:
        (prepare if args.action == 'prepare' else check)(args.directory)
    except (AssertionError, ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(1, 'FAIL: ' + str(exc) + '\n')
