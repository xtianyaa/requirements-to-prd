# 逐项审阅记录

本轮由维护者 AI 会话按生成前确定的 rubric 审阅，非盲评，未经过独立人类业务专家复核。pass/partial/fail 仅表示本条标准的审阅结论，不表示系统测试结果。原始输出未按本轮评分修改。

## contacts / baseline

原始输出：[打开](outputs/contacts.baseline.md)。字符数：5255。

| 条目 | 结论 | 输出证据 | 理由 |
|---|---|---|---|
| C-A | pass | outputs/contacts.baseline.md:L14 — 合规联络人、数据安全负责人、经办人、技术联系人、应急联系人 | 五类角色、联系方式、有效期、离职变更和通知/工单用途均保留。 |
| C-B | partial | outputs/contacts.baseline.md:L107 — \| 离职登记 \| 离职日期、在途工单处理方式、接管人 \| 【事实】C02 \| | 提供了字段候选，但将未给定的在途处理方式/接管人标成事实；也没有充分定义各字段控件。 |
| C-C | pass | outputs/contacts.baseline.md:L119 — 校验规则建议：手机号按 11 位格式 | 11位手机、人数、期限和优先级虽有较强建议，但在建议/待确认段落中提出，未将其声明为正式已确认规则。 |
| C-D | partial | outputs/contacts.baseline.md:L99 — ### 5.4 维护动作字段候选 | 页面与动作有分区，但详情字段的只读/编辑条件和离职动作的具体字段条件仍不明确，表格还混用事实标注。 |
| C-E | pass | outputs/contacts.baseline.md:L157 — 此排序为待评审假设。 | 匹配/离职默认策略是明确标为待评审的假设，末尾排除业务确认；不能将这些假设当真实改派承诺。 |
| C-F | partial | outputs/contacts.baseline.md:L172 — 手机号 138****1234 | 给出场景和下一步，但场景1把带星号的录入值判为手机号格式通过，与建议11位格式不自洽；不是一次真实测试。 |

## contacts / skill

原始输出：[打开](outputs/contacts.skill.md)。字符数：7571。

| 条目 | 结论 | 输出证据 | 理由 |
|---|---|---|---|
| C-A | pass | outputs/contacts.skill.md:L79 — 角色名称，未给出各角色的职责边界与使用场景。 | 五类角色与校验/有效期/离职变更/匹配用途保留，且角色名称与职责建议分开。 |
| C-B | pass | outputs/contacts.skill.md:L165 — ### 6.4 新建/编辑 | 字段、控件、默认、条件、反馈和候选属性都具体，未只交缺口表。 |
| C-C | pass | outputs/contacts.skill.md:L91 — 手机号：11 位数字、以 1 开头【建议】 | 具体手机、人数、期限、审核和排序方案均标建议或待确认，未当作原文正式规则。 |
| C-D | pass | outputs/contacts.skill.md:L181 — ### 6.5 离职/变更登记 | 查询/列表/详情/维护与离职动作分开，字段条件和未知项关联 KD 编号。 |
| C-E | partial | outputs/contacts.skill.md:L230 — 预期：取唯一 1 人作为责任人。 | 场景4只有两名在职有效技术联系人，没有二者日期/更新时间等排序输入，却断言能唯一选人；即使规则是候选，具体推演仍缺判据。 |
| C-F | partial | outputs/contacts.skill.md:L279 — 进入详细功能设计或开发前，须先确认第 2 节关键决定 | 已给具体推演且不追加数据库/API，但末尾要求先确认全部关键决定后进入详细设计，与§1.3可作原型/详细设计输入的说法不一致，可先行范围仍不够明确。 |

## notice / baseline

原始输出：[打开](outputs/notice.baseline.md)。字符数：1168。

| 条目 | 结论 | 输出证据 | 理由 |
|---|---|---|---|
| N-A | pass | outputs/notice.baseline.md:L7 — 面向访客提供已发布公告的查询与浏览能力。 | N01-N03 可追踪，已发布范围、查询、详情与返回均有承载。 |
| N-B | pass | outputs/notice.baseline.md:L42 — 输入为空时返回全部已发布公告。 | 查询与详情展示分开，空查询与无匹配有行为；范围明确没有编辑。 |
| N-C | pass | outputs/notice.baseline.md:L49 — 本轮不提供公告的新增、编辑、删除、上下架、审批、登录鉴权、导出等功能入口。 | 未扩建排除功能，也未追加数据库/API。 |
| N-D | partial | outputs/notice.baseline.md:L42 — 按标题做包含匹配（模糊查询） | 包含匹配、空标题正文占位等新增规则没有在各处标成建议；第4节虽标交互建议，但没有覆盖这些规则。 |
| N-E | partial | outputs/notice.baseline.md:L42 — 关键词查询（N01） | 有空查询和空结果预期，但没有固定公告数据与具体正常关键词，不能直接复核命中集合。 |
| N-F | partial | outputs/notice.baseline.md:L51 — ## 4. 交互建议 | 篇幅简明且未声称已实测；没有说明下一步可进入哪些设计活动。 |

## notice / skill

原始输出：[打开](outputs/notice.skill.md)。字符数：2111。

| 条目 | 结论 | 输出证据 | 理由 |
|---|---|---|---|
| N-A | pass | outputs/notice.skill.md:L5 — 需求编号 N01–N03 | 需求来源可追踪，两页和返回对应 N01/N02，范围限定明确。 |
| N-B | pass | outputs/notice.skill.md:L38 — 否（空=查全部已发布公告） | 查询字段可空，详情逐项只读，空结果和重置有行为。 |
| N-C | pass | outputs/notice.skill.md:L8 — 不含数据库表、API、视觉原型。 | 没有添加维护、登录、审批、导出等排除功能。 |
| N-D | partial | outputs/notice.skill.md:L38 — 去除首尾空格后为空视为无条件查询 | 多处建议有标注，但空查询/去空格规则未标建议，结合“事实不加标注”约定仍有事实与候选混用。 |
| N-E | partial | outputs/notice.skill.md:L66 — S1 正常查询命中 | 场景有预期，但正常输入仍是“标题关键词”，未提供固定关键词和公告数据。 |
| N-F | pass | outputs/notice.skill.md:L99 — 原型设计（列表页、详情页、空结果态、返回交互）。 | 字段表与当前任务相关，明确下一阶段，未声称系统已经实现。 |

## project-register / baseline

原始输出：[打开](outputs/project-register.baseline.md)。字符数：5687。

| 条目 | 结论 | 输出证据 | 理由 |
|---|---|---|---|
| P-A | pass | outputs/project-register.baseline.md:L177 — ### 7.2 各界面字段一览 | 查询、列表、详情与表单字段有落点，原需求编号可追踪。 |
| P-B | pass | outputs/project-register.baseline.md:L190 — 推荐 B（保留并仅在提交时按新类型校验）。 | 外包/内部条件和本企业目录明确，旧值处理明确列为待决定候选。 |
| P-C | pass | outputs/project-register.baseline.md:L62 — **缺失 ≠ 0** | 预算单位/精度/非负、零与空不同、日期关系和不预填今天均保留。 |
| P-D | partial | outputs/project-register.baseline.md:L119 — 允许以空表单或部分字段进行暂存。 | §5.3 允许空表单暂存，与§5.5及P05仅名称必填矛盾；提交后只读与无审批已明确。 |
| P-E | pass | outputs/project-register.baseline.md:L37 — 企业项目管理员仅能查询、查看、编辑**本企业**的项目。 | 读取、写入和服务商范围都有限定，并有跨企业拒绝场景，不仅隐藏按钮。 |
| P-F | partial | outputs/project-register.baseline.md:L208 — **场景 B：外包项目的完整流程** | 零预算、缺服务商、日期倒置和草稿都有具体输入；缺少已提交后尝试改写的独立反例。 |

## project-register / skill

原始输出：[打开](outputs/project-register.skill.md)。字符数：7372。

| 条目 | 结论 | 输出证据 | 理由 |
|---|---|---|---|
| P-A | pass | outputs/project-register.skill.md:L87 — ### 2.5 项目表单页 | 各页与字段、动作、来源和需求映射完整，展示与输入用途可区分。 |
| P-B | pass | outputs/project-register.skill.md:L14 — 切回「内部」时**清空服务商** | 旧值清理标为候选；内外包条件与本企业目录明确，不任取同名服务商。 |
| P-C | partial | outputs/project-register.skill.md:L109 — 仅校验**名称非空**；其余字段不校验、可留空。 | 预算和日期的总体定义正确，但暂存明确不校验其他字段，未区分“可缺项”和“已填非法值”，使非法预算/日期可暂存。 |
| P-D | pass | outputs/project-register.skill.md:L34 — 全部业务编辑字段只读 | 暂存/提交必填分开，提交后所有业务字段只读，没有审批或擅增撤回。 |
| P-E | pass | outputs/project-register.skill.md:L189 — 不可见、不可操作（仅本企业） | 读写范围、关联目录和跨企业拒绝都有说明，不只依赖按钮隐藏。 |
| P-F | pass | outputs/project-register.skill.md:L188 — \| F7 \| P01 \| 管理员，已提交项目 \| 尝试编辑 \| | T1/T4与F3/F6/F7覆盖草稿、零预算、缺服务商、日期倒置和提交后编辑的文档预期；未追加数据库/API。 |
