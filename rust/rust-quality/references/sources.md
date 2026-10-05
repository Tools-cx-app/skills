# 来源与证据边界

原创归纳，源码均 MIT OR Apache-2.0。固定修订用于研究，不要求用户使用这些版本。

- Clippy `9066dbb89ca01eddd591d03a2b4504ab28d7c26b`：[usage.md](https://github.com/rust-lang/rust-clippy/blob/9066dbb89ca01eddd591d03a2b4504ab28d7c26b/book/src/usage.md)，lint选择、allow、自动fix、restriction组；[在线usage](https://doc.rust-lang.org/clippy/usage.html) 是滚动文档。
- [clippy_config/conf.rs](https://github.com/rust-lang/rust-clippy/blob/9066dbb89ca01eddd591d03a2b4504ab28d7c26b/clippy_config/src/conf.rs)：msrv和CARGO_PKG_RUST_VERSION的当前处理；[配置文档](https://doc.rust-lang.org/clippy/configuration.html)。不能承诺所有历史Clippy版本同样处理。
- [driver.rs](https://github.com/rust-lang/rust-clippy/blob/9066dbb89ca01eddd591d03a2b4504ab28d7c26b/src/driver.rs)：通过rustc回调注册lint；内部MIR开关仅实现细节。
- rustfmt `8c329c074b17a339d487ee08ceb03e9e62829e80`：[README](https://github.com/rust-lang/rustfmt/blob/8c329c074b17a339d487ee08ceb03e9e62829e80/README.md)，格式检查及限制；[formatting.rs](https://github.com/rust-lang/rustfmt/blob/8c329c074b17a339d487ee08ceb03e9e62829e80/src/formatting.rs)，AST解析与模块格式化，不运行程序。
- [cargo check](https://doc.rust-lang.org/cargo/commands/cargo-check.html)、[cargo test](https://doc.rust-lang.org/cargo/commands/cargo-test.html)：编译检查与运行用例的公开工具合约。

检查层次、任务范围控制与diff审阅是从这些工具合约归纳的条件性工作流，不新增上游贡献政策。当前推荐的warning配置可能随Cargo版本变化，优先项目既有配置。
