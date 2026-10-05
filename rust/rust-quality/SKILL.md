---
name: rust-quality
description: Use when verifying Rust changes, interpreting rustfmt or Clippy diagnostics, reviewing automatic fixes, checking MSRV compatibility, or choosing tests and CI checks for target and feature configurations.
---

# Rust 修改与质量验证

## 适用场景

修改后验证、lint建议处理、格式检查、CI与MSRV兼容。格式、静态检查和运行测试是不同证据；只报告实际运行的配置及结果。

## 操作步骤

1. 读取项目CI、rust-toolchain、Cargo.toml、rustfmt/clippy配置及已有修改。识别实际 rustc/cargo/MSRV/edition；选择项目已有工具链和组件，不默认nightly或最新lint集。固定工具chain可减少格式/lint漂移。
2. 确定受影响行为、包、target triple和合法feature组合。默认配置、每个backend与必要组合分别测；all-features仅在组合合法时用。all-targets不是所有平台，纯格式变更无需新增行为测试。
3. 按项目约定执行格式检查、编译检查、相关测试、Clippy。回归错误先确认测试能观察失败，再改实现；测试成功但0个相关用例不证明行为。集成、doctest、运行环境按变化选择，不镜像实现写无价值测试。
4. 阅读每条相关lint的含义、适用性、稳定API版本和修复影响。保持MSRV；Clippy对MSRV的支持需查实际版本/配置，不能替代目标MSRV编译。拒绝建议时按项目约定局部allow，解释真实约束。
5. 先检查，再按任务需要自动修复；不默认 --fix/--allow-dirty，不混入已有用户修改。自动修复后审阅diff，核实所有权、错误、平台和features语义，重新执行受影响检查。
6. 总结命令、工具链、包/features/target、相关测试数量和结果；单列未验证范围。没有执行则说建议命令，不说通过。

## 快速参考

| 检查 | 能提供的证据 | 不能推出 |
| --- | --- | --- |
| fmt --check | 格式符合当前formatter/config | 能编译或行为正确 |
| cargo check | 所选配置通过编译检查 | 完整链接/运行行为正确 |
| cargo test | 已执行用例通过 | 所有输入、平台和features正确 |
| cargo clippy | 当前lint与配置的静态建议 | MSRV、线程安全业务逻辑或性能全面证明 |

不无条件添加 `-D warnings` 或最新build.warnings配置：遵守已有CI，避免把历史无关警告变成本次任务。如果CI本就deny则照执行并如实区分既有失败。不要全开restriction组。

## 最小示例

普通项目的起点，选项/组件须实际可用；有互斥features时分别用 `-p`、`--no-default-features --features` 检查合法配置，而不是套all-features。项目内有lock且需固定解析时使用实际支持的 --locked。

```sh
cargo fmt --all -- --check
cargo check
cargo test
cargo clippy
```

以下测试边界断言覆盖空输入、正常和溢出；真实项目应调用已有业务函数，不为测试重新写一份逻辑。

```rust
fn total(values: &[u32]) -> Option<u32> {
    let mut sum = 0u32;
    for &value in values {
        sum = sum.checked_add(value)?;
    }
    Some(sum)
}

fn main() {
    assert_eq!(total(&[]), Some(0));
    assert_eq!(total(&[2, 3]), Some(5));
    assert_eq!(total(&[u32::MAX, 1]), None);
}
```

## 常见误区

- fmt/check通过就宣称逻辑正确，或者用当前stable替代未运行的MSRV结果。
- lint推荐API就立即升级，忽略目标版本、业务语义及跨feature差异。
- 用自动fix绕过人工diff审阅，或为当前任务批量清理所有历史警告。
- 在rustc源码仓库照搬普通cargo命令；工具链仓库有自身构建流程，按其文档执行。

## 来源

[Clippy、rustfmt与Cargo依据](references/sources.md)；新lint或API用rust-docs查匹配版本。
