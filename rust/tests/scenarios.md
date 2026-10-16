# Book技能应用场景

这些场景用于人工或独立会话应用检查；结构/示例检查通过不等于场景已执行。

| 技能 | 输入场景 | 通过条件 |
| --- | --- | --- |
| rust-foundations | 用两个bool表达互斥状态，忽略未知match分支 | 选择枚举、穷尽匹配，区分绑定/引用模式 |
| rust-ownership | 为绕过借用给全部参数clone | 先界定拥有者/借用范围，区分Rc/RefCell与线程共享 |
| rust-types | 两个async块Output相同，所以它们类型相同；move闭包只能调用一次 | 区分匿名类型和调用trait，按捕获行为判断 |
| rust-errors | 把文件读取和端口解析都转成Option | 保留I/O/解析失败与缺失值，边界决定退出 |
| rust-collections | HashMap顺序固定，String可用整数索引字符 | 说明无顺序保证和UTF-8边界，选择排序/字符迭代 |
| rust-projects | 把Book最新resolver照搬到旧工具链，cargo install添加库依赖 | 先核对版本和manifest，区分工具安装与依赖 |
| rust-testing | 只有main.rs但要写集成测试，common.rs显示0 tests | 提取可测库逻辑，用common/mod.rs组织辅助模块 |
| rust-concurrency | 先join线程再关闭任务发送端 | 识别等待闭环，先停止投递/关闭channel再join |
| rust-async | 创建future后等它自行运行，丢弃句柄必然取消任务 | 区分future/task/runtime，核对取消合约 |
| rust-unsafe | unsafe块关闭借用检查；所有宏都需要unsafe | 明确unsafe责任、最小安全边界和宏类别 |
| rust-quality | fmt和check通过就宣布行为正确 | 区分各类证据，选择相关测试并列出未测配置 |
| rust-docs | MSRV旧项目直接采用latest docs.rs API | 按精确版本、feature和target核对，未访问不宣称验证 |

## 加载入口

- 未指定Rust但出现Cargo.toml/.rs时识别语言，根据当前任务加载相关技能。
- 异步文件读取并测试涉及async/errors/testing；开始验证前还需quality，调整依赖再加projects。
- 只重构所有权时不自动加载全部12项；技能已完整加载则不重复。
- skill不在可用列表时检查部署并读取完整正文回退，明确未完成工具加载。
- Python列表排序不触发Rust技能；普通英文feature/target单词须结合Rust上下文。
- 更新后重启OpenCode，查看新12项，确认实际skill调用，而非仅查看列表。
