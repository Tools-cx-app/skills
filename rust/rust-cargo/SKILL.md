---
name: rust-cargo
description: Use when Rust projects have dependency or feature surprises, workspace and resolver questions, lockfile changes, MSRV build failures, target-selection issues, or requirements for locked, offline or reproducible Cargo builds.
---

# Cargo 依赖与构建

## 适用场景

依赖、features、workspace、resolver、锁文件或构建配置问题。Cargo负责包图和构建调度，rustc负责单个crate编译；包feature、Cargo自身不稳定feature和Rust语言feature不是一回事。

## 操作步骤

1. 用项目环境的 `rustc --version --verbose`、`cargo --version` 识别实际工具链；阅读 rust-toolchain 文件、Cargo.toml 的edition/rust-version、Cargo.lock和.cargo配置。优先遵守CI与项目约定，不默认nightly，不自行升级或重写lock。
2. 确认包、target triple、profile、features与依赖类型。裸版本要求如1.28.2通常是caret，已锁版本以lock/解析结果为准；有多个版本时按PackageId分开追踪。包名与crate import名不一定一致。
3. 按实际Cargo/edition查询resolver规则：虚拟workspace没有根package.edition可推导resolver，应明确配置；不从成员edition自动推导。resolver2/3行为需目标版本支持，不无条件改成最新。rust-version是声明，不替代实际MSRV编译。
4. features通常按同一解析单元联合，设计应可叠加；resolver版本可能分离host/build/dev/target上下文。default-features=false仅限制该声明，不是全图否决；workspace继承与member覆盖规则版本敏感，检查两个声明并查匹配版本文档。
5. 先查询再修改：metadata/tree识别包与实际feature来源；metadata --no-deps只看包声明，不证明完整图；lock不记录最终features，完整metadata也不能替代所有构建上下文。tree缺失于旧Cargo时读取manifest/lock并用已有工具，不要求安装最新Cargo。严格不联网/不改lock的诊断用可用的frozen选项，缓存不全时报失败，不自动回退联网。查询可能取锁或写缓存，不能保证整个文件系统只读。
6. 选择合法feature矩阵：默认、no-default、每个backend和必要组合，以及受影响成员单独/联合构建；互斥feature不只用all-features，需要拒绝的非法组合作为预期失败验证。仅构建的选择不等于测试所有目标平台。依赖调整后审阅manifest/lock差异，再执行项目MSRV与CI检查。

## 快速参考

| 选项/文件 | 合约与边界 |
| --- | --- |
| --locked | 锁文件缺失或需改变时失败；不禁止联网 |
| --offline | Cargo不联网，依赖本地缓存；不保证与在线解析相同 |
| --frozen | locked + offline；缺锁/缓存时可失败 |
| Cargo.lock | 记录解析版本；不是所有工具链都能读取所有lock格式 |
| --all-targets | Cargo目标如lib/bin/test/example；不是所有target triple |
| --all-features | 同时开启选中包features；可能违反互斥配置 |

以上flags也需核对实际Cargo支持。offline/frozen不是安全沙箱，不能阻止构建脚本或外部工具自行联网；lock也不固定系统库、工具链或运行环境。

## 最小示例

在项目根执行。先看命令帮助确认选项；tree命令要求实际Cargo提供该子命令。这些查询不编译；frozen可能因缓存/锁文件失败，不能将失败报告为已验证。

```sh
rustc --version --verbose
cargo --version
cargo metadata --help
cargo metadata --no-deps --format-version 1 --frozen
cargo tree --help
cargo tree --frozen -e features
```

进一步按实际包使用 `-p`，feature归属不清时不把一个包的feature传给整个workspace。编译/测试和build scripts可能产生外部副作用，不能称为只读检查。

## 常见误区

- 修改工具链以“修复”旧Cargo不识别配置，或只改rust-version就宣称MSRV达标。
- 依赖声明关闭defaults，却忽略另一条路径开启；tree默认输出也需匹配实际目标和features。
- 把项目package feature误当 `-Z`/cargo-features；不稳定Cargo内部feature不推广为默认工作流。
- 未经请求执行cargo update、删除lock、改resolver或all-features自动修复。

## 来源

[官方规则与固定源码依据](references/sources.md)。版本敏感规则使用 rust-docs；该技能不可用时查对应Cargo文档和实际命令help。
