# Rust Book Skills

12项中文技能以《The Rust Programming Language》为学习主线，按具体工作加载。先按[加载入口](skill-loading.md)识别任务阶段，再调用对应技能。Book是教学来源；语言精确定义、API、Cargo和lint分别核对Reference、rustdoc、Cargo Book和Clippy文档。

## 技能索引

| 技能 | Book范围 | 触发场景 |
| --- | --- | --- |
| [rust-foundations](rust-foundations/SKILL.md) | 3、5、6、19 | 基础语法、类型、表达式、结构体、枚举、模式 |
| [rust-ownership](rust-ownership/SKILL.md) | 4、15、16部分 | 所有权、借用、生命周期、智能指针、共享 |
| [rust-types](rust-types/SKILL.md) | 10、13、18、20部分 | 泛型、trait、trait object、闭包、函数指针 |
| [rust-errors](rust-errors/SKILL.md) | 6、9、12 | Option、Result、panic、错误传播、CLI错误 |
| [rust-collections](rust-collections/SKILL.md) | 8、13 | Vec、String、HashMap、迭代器、容量 |
| [rust-projects](rust-projects/SKILL.md) | 1、7、14、附录E/G | rustup、模块、Cargo、依赖、features、workspace、发布 |
| [rust-testing](rust-testing/SKILL.md) | 11、12、附录D | 单元/集成/文档测试、测试组织与回归 |
| [rust-concurrency](rust-concurrency/SKILL.md) | 16、21 | 线程、channel、共享状态、Send/Sync、关闭清理 |
| [rust-async](rust-async/SKILL.md) | 17 | async/await、future、task、stream、runtime |
| [rust-unsafe](rust-unsafe/SKILL.md) | 20、附录D | unsafe、裸指针、FFI、安全不变量、宏 |
| [rust-quality](rust-quality/SKILL.md) | 附录D、1、11 | rustfmt、Clippy、检查、CI、MSRV证据 |
| [rust-docs](rust-docs/SKILL.md) | 全书 | Book/Reference/API/Cargo/Clippy文档查询 |

每项技能自带`references/sources.md`。正文提炼开发决策，不复制Book章节。版本、edition、MSRV、target和features依具体项目，不默认nightly或升级。

## OpenCode

本机全局配置注册本目录和[技能加载路由](skill-loading.md)。其他机器将12个技能目录复制到`.opencode/skills/`或`~/.config/opencode/skills/`，并在配置中登记目录与路由文件：

```json
{
  "instructions": ["/absolute/path/to/rust/skill-loading.md"],
  "skills": { "paths": ["/absolute/path/to/rust"] }
}
```

改配置或技能后退出并重启OpenCode；确认技能可见后，仍须在每项工作阶段实际调用对应技能。

## 检查

在本目录运行：

```sh
python3 tests/check.py
```

检查12项技能结构、链接和Rust示例，并用当前`rustc`编译运行示例。它不是Cargo项目集成测试，也不是多版本/MSRV验证。行为场景和实际证据记录见`tests/scenarios.md`与`tests/results.md`。
