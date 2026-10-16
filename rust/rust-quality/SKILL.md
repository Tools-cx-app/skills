---
name: rust-quality
description: Use when verifying Rust changes, running rustfmt, Clippy, tests, rust-analyzer, CI checks, or assessing MSRV and feature-matrix evidence.
---

# Rust 质量验证

## 适用

用于 Book 附录D、第1章和第11章相关工具。格式、编译、测试、lint和MSRV是不同证据。

## 步骤

1. 读取CI、toolchain、manifest、formatter和Clippy配置，记录实际rustc/cargo、edition、MSRV、target和features。
2. 先运行项目约定的格式、编译和相关测试；再按需要运行Clippy或rust-analyzer。
3. 对feature矩阵分别验证合法组合；`all-features`不等于所有平台和所有合法组合。
4. 自动修复前确认范围，审阅diff，再重复受影响检查；不默认`--fix`或升级工具链。
5. 报告命令、配置、测试数量、警告和未验证范围；没有运行的检查只列为建议。

Book附录D分别介绍`cargo fmt`、`cargo fix`、`cargo clippy`和rust-analyzer：格式化统一风格，fix应用编译器可用建议，Clippy给静态诊断，语言服务器提供导航/补全/行内诊断。IDE无红线不替代CI。组件缺失先报告环境，不默认安装；自动fix尤其edition迁移应单独审阅，保持项目已有警告策略。

## 示例

```sh
cargo fmt --all -- --check
cargo check
cargo test
cargo clippy
```

## 误区

- fmt通过不证明能编译，编译通过不证明行为正确。
- Clippy建议不是MSRV或性能证明；lint类别和参数按安装版本核对。
- `cargo clippy --fix`可能扩大目标范围；自动修改必须人工审阅。
- `cargo test`不覆盖未选择的feature、target或外部环境。

## 来源

[Book附录D](https://doc.rust-lang.org/book/appendix-04-useful-development-tools.html)、[Cargo test](https://doc.rust-lang.org/cargo/commands/cargo-test.html)、[Clippy Book](https://doc.rust-lang.org/stable/clippy/)、[rustfmt](https://github.com/rust-lang/rustfmt)。
