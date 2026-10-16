# Rust 技能加载

处理Rust项目或Rust问题时，在开始对应分析、设计、文件读取后的结论、编辑或命令前，按表调用`skill`。Rust信号包括`.rs`、`Cargo.toml`、`Cargo.lock`、`rust-toolchain*`、`.cargo/`、`build.rs`、`rustc`、`cargo`、`rustup`、`rustfmt`、`clippy`、edition、MSRV、crate、feature、workspace、target、async/await、unsafe、trait或宏。可用列表、description、旧记忆不算加载；当前上下文已完整加载的技能不重复。

| 工作内容 | 技能 |
| --- | --- |
| 基础语法、类型、模式、结构体、枚举、控制流 | rust-foundations |
| move/borrow、生命周期、智能指针、Drop、共享所有权 | rust-ownership |
| 泛型、trait、闭包、trait object、函数指针 | rust-types |
| Option/Result、panic、错误边界和传播 | rust-errors |
| Vec/String/HashMap、迭代、容量、计数 | rust-collections |
| 包/模块、依赖、Cargo、feature、workspace、发布 | rust-projects |
| 单元/集成/doc测试、测试组织、回归测试 | rust-testing |
| 线程、channel、Send/Sync、共享状态、线程池 | rust-concurrency |
| async/await、future、任务、stream、runtime | rust-async |
| unsafe、裸指针、FFI、安全不变量、宏 | rust-unsafe |
| rustfmt、Clippy、编译、CI、验证与MSRV检查 | rust-quality |
| Book、Reference、Edition Guide、API/工具文档查询 | rust-docs |

## 执行顺序

1. **发现**：从用户请求、文件、命令和代码识别全部Rust工作阶段；不要等错误出现。
2. **加载**：进入对应阶段分析、设计、比较方案或编辑前调用表中技能。一个阶段命中多项时先加载全部相关技能。
3. **执行**：依据已加载正文工作；不要因为任务简单、用户没点名或预计符合例外而跳过加载。
4. **补加载**：阅读项目发现新阶段时暂停，先加载新相关技能；例如改feature加载rust-projects，开始测试加载rust-testing/rust-quality。

只加载相关技能，不因使用Rust而加载全部12项。例如异步文件读取并测试加载rust-async、rust-errors、rust-testing；涉及依赖时再加载rust-projects。仅修改所有权时不自动加载无关技能。

应加载技能不在列表时暂停，检查路径、`SKILL.md`、skill权限和是否需要重启。文件可读则完整读取正文回退，并明确说明工具调用未成功；不能只读description或假称已调用。无法取得正文则说明缺失并遵循现有项目指令。更改路由/技能后退出并重启OpenCode；旧会话不算重新加载。
