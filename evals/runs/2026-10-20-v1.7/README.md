# v1.7 首轮对照记录

日期：2026-10-20（Asia/Shanghai）。状态：三组样本、六份实际生成输出已记录；结论限于本次小规模实验。

本次观察到技能组字段/来源/阶段说明更充分，但三组输出都更长，且仍有规则与场景不自洽的问题。不能据此声称技能普遍提高质量，也不能据此批准生产开发。

## 输入与输出

| 样本 | baseline 原始输出 | skill 原始输出 | 字符数 baseline / skill | 审阅 pass / partial / fail（两组各6项） |
|---|---|---|---|---|
| [输入：notice](cases/notice/input.md) | [baseline](outputs/notice.baseline.md) | [skill](outputs/notice.skill.md) | 1168 / 2111 | 3/3/0；4/2/0 |
| [输入：project-register](cases/project-register/input.md) | [baseline](outputs/project-register.baseline.md) | [skill](outputs/project-register.skill.md) | 5687 / 7372 | 4/2/0；5/1/0 |
| [输入：contacts](cases/contacts/input.md) | [baseline](outputs/contacts.baseline.md) | [skill](outputs/contacts.skill.md) | 5255 / 7571 | 3/3/0；4/2/0 |

这些计数不是通用质量分或开发就绪率。逐项理由和原文定位见 [REVIEW.md](REVIEW.md)，机器记录见 [results.json](results.json)，不可只看汇总数字。

## 本次仍发现的问题

- 公告：两组都没有给正常查询的固定关键词与公告集合；部分新增规则没有就近标为建议。技能组从1168字符增至2111字符，细则更充分但不意味着更精炼。
- 项目台账：baseline 同时写“空表单可暂存”和“名称必填”；skill 写“其余字段不校验”，没有区分草稿可缺项与已填非法值。技能组的边界场景更完整，但仍需修正草稿格式校验。
- 联系人：baseline 将未给定的接管字段标成事实，且用带星号的手机号录入值断言格式通过；skill 的多候选输入不足以唯一选人，却预期选出唯一责任人，并对可先行详细设计给出不一致表述。
- 已明确标为候选的11位手机、人数、有效期等设计，没有仅因其为候选就判失败；它们仍需业务选择，不能作为通用规则推广。

## 执行条件与溯源

- baseline：同一需求与交付要求，不在请求中提供 requirements-to-prd 规则；skill：额外全量注入 SKILL.md 与4份参考文件。
- 全量注入不等于原生技能发现/渐进加载。两组的公共委派包装与工具条件相同，但宿主全局系统提示、提供方路由和内部采样参数没有完全审计。
- 经 Codex 子任务 -> codex-with-cc 委派 -> 本机 Claude Code CLI 执行。CLI system/init 版本为2.1.79；CLI 选择别名为sonnet，六次返回的 model 字段均为 deepseek-v4-pro。这里只记录宿主返回值，不能独立核实后端模型身份，不能称为 Claude Sonnet 评测。
- 六个成功生成会话的 initialResume/resume 均为false，session身份哈希互不相同；每份输出来自一次成功生成，不按评分返工。
- contacts-skill 先有两次未进入模型的环境失败：沙箱目录权限失败、无效会话恢复。随后一次重置请求在执行前被自动审批拒绝；经用户直接批准后，新会话只补跑一次并成功。失败类别、时间与RunId保留在 results.json，未伪装成模型质量失败或隐藏重试。
- 输入、rubric、规则快照与请求的SHA256见 [prepared.json](prepared.json)。本轮技能正文与v1.7一致，仅新增MIT许可元数据；快照哈希用于精确定位实际注入内容。
- UTC起止、CLI报告的usage/成本（若返回）、文件字节哈希、运行ID及产物核验退出码见results.json。它们是宿主报告，不作为标准计费或性能承诺。
- 仅发布虚构输入和生成正文及脱敏元数据。未发布凭据、本机绝对路径或完整宿主日志；完整运行日志由本机维护者保留。

## 复现与局限

按 [评测协议](../../README.md) 准备新目录；使用本目录的 *.prompt.md 在同一工具/模型的新会话中重放，保持两组公共要求一致。当前运行还附加了只写output.md、不读其他运行/评分表、不搜索外网以及按委派合同收尾等公共约束；宿主自身系统提示不包含在公开请求中。换宿主或后端应记录为新实验。

评分是维护者AI非盲审阅，不是独立人工验收；只有三个合成样本、单次生成、单一报告模型ID，未做跨模型或多次统计实验。输出长度与字段覆盖只用于描述，不能替代业务判断。下一步应让独立评审者复核 partial 项、加入更复杂样本，并做重复/跨模型对照。

## 完整性检查

v1.7.1 打包修正仅将本记录中的 `snapshot/SKILL.md` 改名为 `snapshot/skill-definition.md`，并增加存储映射，避免安装时重复发现技能。原始输入、注入请求、快照内容、模型输出和评分均未因此改变；本记录仍属于 v1.7 首轮评测。

```bash
python scripts/eval_bundle.py check evals/runs/2026-10-20-v1.7
```

该命令只核验文件、哈希、案例/组别与评分记录完整性，不判定上述业务评分正确。
