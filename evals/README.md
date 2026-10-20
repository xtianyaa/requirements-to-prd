# 评测与公开样本

本目录维护合成需求、评分标准和实际模型输出，用于检查技能是否改善 PRD 的业务质量。输入不来自客户文件；公开样本均为虚构业务，不包含真实企业、人员或联系方式。

- [文字回归场景](scenarios.md)：8 个维护用场景，覆盖常见设计错误。
- [公告浏览输入](cases/notice/input.md) / [评分标准](cases/notice/rubric.json)：简单需求不扩建。
- [项目台账输入](cases/project-register/input.md) / [评分标准](cases/project-register/rubric.json)：字段、条件必填、状态和企业范围。
- [联系人输入](cases/contacts/input.md) / [评分标准](cases/contacts/rubric.json)：稀疏材料下的候选与未知边界。

每份输出是一次实际生成记录，不是唯一正确的标准 PRD。评测以业务不变量为准，不要求模型复现章节、措辞或表格样式。已有运行结果见 [runs/](runs/)；结果的适用范围以各次报告为准。

首轮实际记录：[2026-10-20 / v1.7](runs/2026-10-20-v1.7/README.md)。含6份未改写输出及36条逐项AI审阅，未经过独立人工业务复核。

## 对照协议

1. 评分标准先于本轮模型生成确定；生成者不读取评分文件、其他组输出或本轮人工结论。
2. 每个样本分别运行 baseline 和 skill。原始输入与任务要求相同；skill 组额外得到技能正文和参考规则。
3. 同一对照使用相同模型选择、宿主和权限/工具条件，独立新会话，不复用历史。记录实际报告的模型 ID、UTC 时间、激活方式和异常；别名或提供方转发不能证明真实模型身份。
4. 保留第一次完成的原始输出，不为提高成绩偷偷改写。重跑必须新增记录并说明原因，失败不得只留下成功重试。
5. 评审者按 rubric 逐项标 `pass`、`partial`、`fail` 或 `not-assessed`，附输出中的定位/摘录和理由。记录评审者是人类、模型还是维护者 AI 会话，以及是否盲评；AI 审阅不能标成人工业务验收。合成样本上的局部通过不代表业务确认、系统验收或通用质量提升。
6. 完整记录会话条件和局限。全量注入规则只评测指令效果，不算宿主原生技能发现、渐进加载或跨平台兼容性验证。未控制的宿主系统提示和模型随机性须披露。

## 准备可移植请求

需要 Python 3.10+，无第三方包。以下操作不调用模型、不产生推理费用：

```bash
python scripts/eval_bundle.py prepare /path/to/new-run
```

目标目录必须不存在，防止覆盖已有证据。脚本保存输入、rubric、技能快照、两组请求和 SHA256 清单。为便于跨平台重放，输入与规则快照统一为 UTF-8、LF 换行。

技能快照以 `skill-definition.md` 保存，避免被工具当作新的技能入口。`prepared.json` 的 `snapshot_files` 将逻辑来源名映射到存储文件名；哈希仍对应原内容。旧版未提供映射的记录也可核验。

将每个 `*.prompt.md` 原样送入独立会话，把生成的 `output.md` 保存到运行目录下。两组保持相同工具条件；不要给生成者 rubric。请求采用**全量规则注入**，与原生按需加载不同。使用自己的模型 CLI/API 时，按对应工具文档调用；本仓库不绑定模型厂商、不读取 API 密钥，也不提供一个假装通用的执行命令。

## 记录与核验

在运行目录中保存 `results.json` 数组，每项对应一个 `case_id` 与 `arm`，至少包含：

```json
{
  "case_id": "notice",
  "arm": "baseline",
  "model_reported": "填写实际返回值，无法获得则明确 unavailable",
  "timestamp_utc": "填写实际运行时间",
  "session_fresh": true,
  "reviewer_type": "填写 human、independent-model 或 maintainer-assistant",
  "review_blinded": false,
  "output_file": "outputs/notice.baseline.md",
  "output_sha256": "填写实际文件哈希",
  "ratings": [
    {
      "id": "N-A",
      "result": "pass",
      "evidence": "填写输出中的章节/行及摘录",
      "reason": "说明如何满足或违反本项"
    }
  ]
}
```

上面仅示意格式，不是一次评测结果；实际记录必须包含该样本的全部 rubric 条目，不能省略未通过项。可添加运行时长、CLI 版本、模型参数、成本或 token 统计；工具没有返回的值写未知，不反推或编造。

完成记录后运行：

```bash
python scripts/eval_bundle.py check /path/to/run
```

检查器验证文件哈希、案例/组别完整性和判分记录字段，**不会判定 PRD 业务正确性，也不会证明评审证据真实**。缺少独立复核或重复实验时应在结论中写明，不将单次小样本评测写成效果保证。
