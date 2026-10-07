# Rust 技能加载入口

处理Rust项目或Rust问题时，在开始对应分析、设计、编辑或执行命令前，按任务内容通过skill工具加载相关技能。Rust信号包括`.rs`、`Cargo.toml`、`Cargo.lock`、`rust-toolchain*`、`.cargo/`、`build.rs`、`rustc`、`cargo`、`rustup`、`rustfmt`、`clippy`、edition、MSRV、crate、feature、workspace或target。技能出现在可用列表不等于已加载；记得其内容、熟悉Rust、任务简单或用户没说技能名，都不替代加载。已在当前上下文完整加载的技能无需重复调用。

| 即将进行的工作 | 必须加载 |
| --- | --- |
| 实现新功能、选择依赖或打算自写工具/算法/解析器 | rust-crates-first |
| 设计或修改所有权、借用、生命周期、clone、智能指针、线程共享 | rust-ownership |
| 设计或修改Result/Option、错误传播、panic或失败处理 | rust-errors |
| 选择/修改集合、迭代、顺序、计数或容量 | rust-collections |
| 修改/排查Cargo.toml、依赖、features、workspace、锁文件或构建配置 | rust-cargo |
| 查询/判断语言规则、API可用性、版本、MSRV或feature gate | rust-docs |
| 验证Rust修改、选择/运行fmt、Clippy、测试或CI检查 | rust-quality |

## 强制时序

1. **发现**：从用户请求、文件名、命令和读取到的代码识别Rust及相关工作；不要等编译报错或看到关键词才判断。
2. **加载**：在进入该工作的分析、设计、方案比较、文件读取后的结论、编辑或命令执行前，实际调用对应的`skill`。只要一个阶段涉及多个表格行，先加载全部相关技能。
3. **执行**：只能把已加载技能正文作为该阶段依据；技能调用失败时按末条回退，并明确回退状态。
4. **补加载**：阅读项目后发现新的工作，立即暂停进入新工作的行动，先补调用；例如实现过程中开始改Cargo features，先加载rust-cargo；准备测试或Clippy，先加载rust-quality。

用户只说“加功能”“修复”“重构”时也根据实际代码内容匹配，不必等出现borrow/Result等关键词；不要把所有技能一次全加载，也不要把只读description、列表可见或旧会话记忆算作加载。

例如“新增读取配置并统计项目”：分析需求前加载rust-crates-first；进入读取失败处理、集合计数时分别加载rust-errors、rust-collections；如果需要调整serde features再加载rust-cargo；运行检查前加载rust-quality。技能里的标准库/已有实现、自写等例外在加载后判断，不能以预计会符合例外而跳过加载。仅查看文档/API规则时加载rust-docs；只改所有权或线程共享时不因使用Rust就自动加载全部技能。

若应加载的技能不在可用列表，暂停对应工作，检查安装路径、`SKILL.md`、skill权限和是否需要重启；如文件可访问，读取相应`SKILL.md`完整正文作为回退，并说明“skill工具加载未成功，已读取正文回退”。无法取得正文时说明缺失，遵循现有项目指令，不假称已应用。加载配置、技能文件或路由规则改变后，退出并重启OpenCode；重启前的旧会话不算重新加载。
