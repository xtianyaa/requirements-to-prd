"""Integrity-tool tests only; these fixtures are NOT model evaluation results."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'scripts/eval_bundle.py'


class EvalIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='prd-integrity-test-')
        self.run = Path(self.temp.name) / 'run'
        self.addCleanup(self.temp.cleanup)
        self.assertEqual(self.call('prepare').returncode, 0)

    def call(self, action):
        return subprocess.run([sys.executable, '-X', 'utf8', str(TOOL), action, str(self.run)],
                              capture_output=True, text=True, encoding='utf-8')

    def seed_records(self):
        manifest = json.loads((self.run / 'prepared.json').read_text(encoding='utf-8'))
        rows = []
        for r in manifest['records']:
            output = self.run / 'outputs' / (r['case_id'] + '.' + r['arm'] + '.md')
            output.parent.mkdir(exist_ok=True)
            output.write_bytes(b'INTEGRITY TEST ONLY; NOT MODEL OUTPUT\n')
            rubric = json.loads((self.run / 'cases' / r['case_id'] / 'rubric.json').read_text(encoding='utf-8'))
            rows.append(dict(case_id=r['case_id'], arm=r['arm'], model_reported='test-only',
                             timestamp_utc='test-only', session_fresh=True,
                             reviewer_type='test-fixture', review_blinded=False,
                             output_file=output.relative_to(self.run).as_posix(),
                             output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                             ratings=[dict(id=c['id'], result='not-assessed', evidence='test fixture',
                                           reason='no business grading') for c in rubric['criteria']]))
        (self.run / 'results.json').write_text(json.dumps(rows), encoding='utf-8')
        return rows

    def test_complete_record_and_output_tampering(self):
        rows = self.seed_records()
        self.assertEqual(self.call('check').returncode, 0)
        (self.run / rows[0]['output_file']).write_bytes(b'tampered')
        result = self.call('check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('FAIL:', result.stderr)

    def test_preserve_existing_evidence(self):
        old = (self.run / 'prepared.json').read_bytes()
        self.assertNotEqual(self.call('prepare').returncode, 0)
        self.assertEqual((self.run / 'prepared.json').read_bytes(), old)

    def test_missing_case_is_not_a_complete_run(self):
        rows = self.seed_records()
        (self.run / 'results.json').write_text(json.dumps(rows[:-1]), encoding='utf-8')
        self.assertNotEqual(self.call('check').returncode, 0)

    def test_snapshot_does_not_register_another_skill(self):
        self.assertEqual(list(self.run.rglob('SKILL.md')), [])
        self.assertTrue((self.run / 'snapshot/skill-definition.md').is_file())


if __name__ == '__main__':
    unittest.main()
