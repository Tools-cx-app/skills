# 验证记录

## stable Reference代码规则更新

- 2026-10-05读取用户指定Reference入口及expressions、patterns、destructors、operator-expr、loop-expr、conditional-compilation、interior-mutability、panic相关内容；查询式返回缺内容的页面改为读取正文，避免从“未抽取到”推断规则不存在。
- 修改前定位任务 `ses_ef615d17fffe06hG3I2WvkqWgO` 识别原技能缺少部分移动/Drop、临时值/edition、?闭包边界、for协议、cfg!及溢出例外，提取运算符正文证据。
- 修改后任务 `ses_ef6110014ffeSMPT79H7GdKQDB` 正确应用六项代码规则及来源边界；据其复核收紧Copy/按值表述、部分移动重新初始化条件、数组2015/2018及优化可观察行为约束。
- Reference用于语言语义，不把标准库容器/API、Cargo依赖或用户crates-first规则改写为其风格建议。latest stable不替代历史工具链/edition核验。
- 本轮未改变示例逻辑，使用既有四个完整Rust示例检查；未实测所有版本/平台或每个文字规则的编译反例。

## stable Clippy 文档更新

目录已由用户重命名：技能包现为 `/home/tweaks/skills/rust`，编译器源码为 `/home/tweaks/skills/rust-lang`；早期记录中的distilled路径为历史执行位置。

- 已读取用户指定stable入口及usage/configuration，修改rust-quality的分类、默认等级、配置搜索、等级与参数区分、MSRV、fix和依赖范围；rust-docs增加Clippy版本查询入口，README修复加载路径。
- 修改前测试 `ses_ef6206097ffeOwxXWbUZplc720` 识别原技能未覆盖all边界、九类等级、配置搜寻、no-deps参数位置、fix隐含范围及CI旧新规则。
- 修改后测试 `ses_ef61d0757ffehgb7k8d8XlsXtH` 正确应用上述规则，区分1.70旧方式与新配置、master与安装版，未声称执行检查。源页面已由主会话实际读取；补录warning策略原句用于追溯。
- 当前会话的技能加载可能仍来自启动时旧内容；磁盘内容检查通过不表示运行会话已重新加载。安装配置需指向新目录并重启OpenCode。

## 环境与方法

- rustc 1.101.0-nightly (0abfedbc7 2026-10-02)
- cargo 1.101.0-nightly (f3865b2a4 2026-09-29)
- 场景见 [scenarios.md](scenarios.md)。基线代理任务 ID：ses_ef68131eaffeaiSQbSCFrkW24w。
- 基线未读技能、未联网；评分来自主会话人工审阅原始回复，不是代理自评分。
- 本包是 reference skills。检索/应用测试与示例执行可验证可用性，不能据单次代理测试声称普遍改善。
- 上述 rustc/cargo 版本仅为本次执行环境，不是技能的版本要求。技能使用项目工具链和 MSRV；未实际运行的版本不宣称通过。

## 无技能基线

| 主题 | 实际结果 | 原始证据与缺口 |
| --- | --- | --- |
| ownership | 核心语义通过 | “Arc 只解决共享所有权，不会自动让内部类型线程安全”；识别 scope 从1.63稳定。未表现出必须由技能修复的错误。 |
| errors | 核心语义通过 | 给出 Result<Option<u16>, PortError>，识别 .ok() 丢错误，标明端口0的业务含义。未表现出必须由技能修复的错误。 |
| collections | 部分失败 | 原问题 Vec::with_capacity(10)，回复却写“HashMap::with_capacity(10)”并引用HashMap来源；计数“+= 1”未说明溢出条件。 |
| cargo | 核心语义通过 | “虚拟 workspace 不会自动从成员的 edition 推断 resolver”；locked与offline分清。未表现出必须由技能修复的错误。 |
| quality | 部分失败 | 默认Clippy命令追加“-D warnings”，未充分处理已有无关warning与任务范围，缺少修复后的明确diff审阅步骤。 |
| docs | 核心语义通过 | “不要用 latest 页面代替历史版本证据”；正确处理 feature 联合。另将已知“锁定”拓展为manifest caret提醒，需避免抹掉题目已给定事实。 |

通过的基线不伪造成RED失败；相应技能为来源支持的参考整理，不宣称其能修复已观察到的行为缺陷。失败项用于约束容器类型匹配、溢出条件、lint检查范围与审阅步骤。

## 加载技能后的应用验证

| 技能 | 任务ID | 结果与实际修订 |
| --- | --- | --- |
| ownership | ses_ef67a7245ffeQfTD46K4ah9KHv；ses_ef6779db5ffeG5HEz988W2mCzZ | 正确区分RefCell Send/!Sync、Arc边界、MSRV1.60替代、Vec<Arc<T>>非深拷贝。补充普通spawn立即join仍需static和无既有scoped依赖时的约束冲突。 |
| errors | ses_ef67503faffepUu6GX0MfHwy4y | 正确保留IO/Parse/缺失三态，解释0的业务规则及UTF8归类；补充InvalidData与版本查询fallback。 |
| collections | ses_ef6721415ffeUuUtGohef5XBci | 正确回答Vec容量≥10、Entry、无界流checked_add，并提出资源预算与有序追加反例；补充1.53数组迭代门槛及容器特定分配恢复边界。 |
| cargo | ses_ef66eb081ffeY4dyjjXvh0yY8d | 正确区分联合/defaults、虚拟resolver、locked/offline/frozen、版本敏感继承规则；补充metadata/lock能力边界、成员联合矩阵和缓存副作用。 |
| quality | ses_ef66bb13affeBcXgOxxHKsaSkw | 未默认all-features/fix/allow-dirty/deny全部warning，明确人工diff与MSRV复测；纯格式不新增行为测试，不为CLI升级。 |
| docs | ses_ef66848ffffebxrUl2FYvcXeDS | 按锁定1.28.2查询，不假装访问；区分features/target、docs.rs非默认all-features与nightly不证明MSRV。补充cfg(doc)、陈旧文档和frozen非只读/沙箱。 |

初始应用测试后的小补充主要澄清已识别边界；最终包另经fresh-context合并反例复测及全量结构/示例检查。测试代理只做读取与分析，未编译其输出方案，也未修改文件。

最终合并复测任务：`ses_ef6651206ffeqv1FrPXpDCLEfC`。六项核心语义与版本条件均PASS；主会话审阅实际逐项决策，确认低版本scoped约束冲突、RefCell Send/Sync、三态错误、无界计数、合法feature矩阵、历史警告处理与未查询文档的条件结论。该结果不代表所有未来模型或任务都能正确应用。

## 可重复检查与局限

- `python3 tests/check.py rust-ownership` 初始运行因SKILL.md不存在而失败，观察到结构检查RED；随后各项创建后分别运行成功。
- 检查脚本只对完整内嵌Rust代码进行真实编译/运行；Cargo/shell命令是项目条件示例，本次无目标业务项目，不伪造执行成功。
- Python检查无需YAML库，只覆盖本包使用的简单frontmatter形式，不是通用YAML解析器。
- 基线中的collections容量错引属于直接观察缺口；quality缺少审阅属于范围/完整性问题。其余核心基线通过，不声称所有技能都有RED→GREEN行为改进。
- 新旧版本通用策略经过场景验证；没有逐版本安装运行，不宣称多版本兼容已实测。

## 第七项：rust-crates-first

- 基线任务 `ses_ef6598cf6ffe0E5d6MNdedNsug` 已选择先查询cron crate，尊重明确自写及std例外；未观察到一般查询缺失。但其断网分支写“若期限迫使采用自写方案，应基于已确认的有限需求作出取舍”，允许未经用户明确自写例外而按期限自行决定，未满足本项严格规则。
- 压力复测 `ses_ef655c91cffe8I9GWf7jsHXD3t` 明确暂停自写、先查询；超时不证明无crate，负责人催促不自动授予例外；兼容历史版本、私有registry、std/已有依赖和明确自写反例均正确处理。
- 据复测补充缓存证据边界、真实用户明确自写不需重复询问，以及本用户规则优先于通用“几行自写更短”偏好。
- 官方cargo-search和cargo-info页面已读取，确认默认registry可改变、info可能创建lock；技能不要求特定Cargo版本或使用info/add。
- 新项结构检查先观察SKILL.md缺失失败；最终纳入七项全量检查。行为压力样本数量有限，未做多次统计实验，不宣称对所有agent可保证执行。
