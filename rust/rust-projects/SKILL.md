---
name: rust-projects
description: Use when Rust work involves rustup, Cargo.toml, packages, crates, modules, paths, visibility, workspaces, profiles, features, publishing, installation, editions, or dependency selection.
---

# Rust 项目与 Cargo

## 适用

用于从包结构到构建发布的项目级决策。以 Book 第1、7、14章和附录E/G为主线。

## 步骤

1. 读取 `rust-toolchain*`、`Cargo.toml`、`Cargo.lock`、`.cargo/`、CI、edition和rust-version；不默认升级工具链。
2. 区分 package、crate、module、路径和可见性；先让模块边界反映职责。
3. 新功能先查询 crates.io；核对精确版本、MSRV、features、target、许可证和维护状态。
4. 用户明确自写/禁止第三方，或标准库/已有依赖已满足时，加载本技能后按例外执行。
5. workspace、resolver、feature和profile修改后审阅完整manifest/lock差异；不未经请求执行全图update。
6. 发布或安装前核对包名、二进制入口、文档、许可证、版本和目标工具链。

## 项目操作

- `src/main.rs`是常见二进制根，`src/lib.rs`是库根；module是命名/隐私边界，文件拆分不是新crate。`use`引入路径，`pub use`重导出公共接口，不能让原本不可访问的路径任意越过隐私。
- workspace共享lock和常见target目录，但成员依赖仍需显式声明；用`-p`选包。Book示例使用resolver3不要求旧项目直接照搬，按Cargo版本和edition选择。
- dev/release profile是可配置构建策略；优化级别、调试和溢出检查独立核对，不把profile名字当行为保证。features和resolver的细节超出Book时查Cargo Book。
- 发布前检查文档示例、`cargo doc`、包内容和semver；`cargo publish`会向registry发布，实际发布须由用户授权。`cargo install`安装二进制工具，不等于给当前包添加库依赖；自定义`cargo-<name>`子命令是外部程序。

## 示例

```sh
rustc --version --verbose
cargo --version
cargo metadata --no-deps --format-version 1 --frozen
cargo tree --help
```

## 误区

- package名、crate名和import名可能不同。
- `--all-features`可能开启互斥配置；不要把它当完整测试矩阵。
- `rust-version`是声明，不是已完成的MSRV验证。
- 网络查询失败只能说明未核实，不能证明没有合适crate。

## 来源

[Book第1章](https://doc.rust-lang.org/book/ch01-00-getting-started.html)、[第7章](https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html)、[第14章](https://doc.rust-lang.org/book/ch14-00-more-about-cargo-and-crates-io.html)、[Cargo Book](https://doc.rust-lang.org/cargo/)。
