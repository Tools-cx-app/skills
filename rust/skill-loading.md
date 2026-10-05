# Rust 技能加载入口

处理Rust项目（Cargo.toml、.rs、rustc/cargo）或Rust问题时，在开始对应分析、设计、编辑或执行命令前，按任务内容通过skill工具加载相关技能。技能出现在可用列表不等于已加载；记得其内容、熟悉Rust、任务简单或用户没说技能名，都不替代加载。已在当前上下文完整加载的技能无需重复调用。

| 即将进行的工作 | 必须加载 |
| --- | --- |
| 实现新功能、选择依赖或打算自写工具/算法/解析器 | rust-crates-first |
| 设计或修改所有权、借用、生命周期、clone、智能指针、线程共享 | rust-ownership |
| 设计或修改Result/Option、错误传播、panic或失败处理 | rust-errors |
| 选择/修改集合、迭代、顺序、计数或容量 | rust-collections |
| 修改/排查Cargo.toml、依赖、features、workspace、锁文件或构建配置 | rust-cargo |
| 查询/判断语言规则、API可用性、版本、MSRV或feature gate | rust-docs |
| 验证Rust修改、选择/运行fmt、Clippy、测试或CI检查 | rust-quality |

开始任务时先判断相关项；阅读项目后发现新的相关工作，进入该工作前补加载。用户只说“加功能”“修复”“重构”时也根据实际代码内容匹配，不必等出现borrow/Result等关键词，不把所有技能一次全加载。

例如“新增读取配置并统计项目”：实现前加载rust-crates-first；进入读取失败处理、集合计数时分别加载rust-errors、rust-collections；运行检查前加载rust-quality。技能里的标准库/已有实现、自写等例外在加载后判断，不能以预计会符合例外而跳过加载。

若应加载的技能不在可用列表，检查安装路径、skill权限和是否重启；如文件可访问，读取相应SKILL.md作为回退并说明工具加载未成功。不要把目录存在或只读description当成加载完成。无法取得正文时说明缺失，遵循现有项目指令，不假称已应用。
