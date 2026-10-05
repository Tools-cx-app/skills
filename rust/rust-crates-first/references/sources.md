# 来源与证据边界

原创流程；“crates.io先查询、自写例外”来自用户确认，不冒充上游政策。

- [cargo search](https://doc.rust-lang.org/cargo/commands/cargo-search.html)：registry文本查询；默认registry可由registry.default更改，默认值crates-io；--registry、--limit及本机help。结果与描述不证明API满足需求。
- [cargo info](https://doc.rust-lang.org/cargo/commands/cargo-info.html)：包manifest信息与精确版本查询；workspace内可能创建lock，无版本时依环境选择版本。不是所有历史Cargo提供，不要求升级。
- [crates.io](https://crates.io/)：包发现和版本元数据；[docs.rs](https://docs.rs/)：精确版本API，features/target需匹配。
- [依赖声明](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html)、[rust-version](https://doc.rust-lang.org/cargo/reference/rust-version.html)、[features](https://doc.rust-lang.org/cargo/reference/features.html)：版本、MSRV与feature合约。MSRV声明不等于整个图实测。

维护、许可、功能、构建成本的评估依项目约束；没有通用下载数或更新频率阈值。滚动文档的CLI能力与crate支持范围必须使用时核实；网络失败或证据不足报告未核实。
