# 来源与证据边界

原创归纳。Cargo修订 `bb2126cffae48394a37db8728dc50a17bbfe54d4`，MIT OR Apache-2.0。当前实现不是旧Cargo行为的保证。

- [Cargo Book features](https://doc.rust-lang.org/cargo/reference/features.html)：可叠加、联合、defaults与互斥features指导。
- [Workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)、[Resolver](https://doc.rust-lang.org/cargo/reference/resolver.html)：虚拟workspace与resolver；workspace依赖覆盖规则应查匹配版本，不以滚动文档承诺所有旧版。
- [cargo build](https://doc.rust-lang.org/cargo/commands/cargo-build.html)：locked/offline/frozen与目标选择合约；[Build scripts](https://doc.rust-lang.org/cargo/reference/build-scripts.html) 说明外部程序执行能力，offline不是进程沙箱。
- [Rust version](https://doc.rust-lang.org/cargo/reference/rust-version.html)、[Specifying dependencies](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html)：MSRV声明与版本要求。
- [resolver/features.rs](https://github.com/rust-lang/cargo/blob/bb2126cffae48394a37db8728dc50a17bbfe54d4/src/resolver/features.rs)：feature解析第二遍与host/dev/target分离，仅实现依据。
- [workspace/features.rs](https://github.com/rust-lang/cargo/blob/bb2126cffae48394a37db8728dc50a17bbfe54d4/src/workspace/features.rs)：Cargo自身稳定/不稳定开关，不是包features。
- [ops/cargo_compile/mod.rs](https://github.com/rust-lang/cargo/blob/bb2126cffae48394a37db8728dc50a17bbfe54d4/src/ops/cargo_compile/mod.rs)：依赖图、UnitGraph、BuildContext/BuildRunner调度，仅源码定位。

feature矩阵和优先只读诊断是条件性开发建议。解析、编译、测试、联网和缓存写入边界必须按具体命令区分。

[stable Reference条件编译](https://doc.rust-lang.org/stable/reference/conditional-compilation.html)于2026-10-05读取：cfg属性条件移除、cfg!布尔展开、feature键为Cargo约定。该文不定义Cargo resolver；新增条件语法/宏不自动适用旧Rust。
