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
4. 按下表识别lint类别，再读具体lint的含义、适用性、版本与修复影响。默认cargo clippy使用clippy::all，不等于开启所有lint。保持MSRV；只有部分lint识别MSRV，它们可能抑制诊断或选择旧版建议，不能替代目标MSRV编译。拒绝建议时按项目约定局部allow，解释真实约束。
5. 先检查，再按任务需要自动修复；不默认 --fix/--allow-dirty，不混入已有用户修改。`cargo clippy --fix`隐含`--all-targets`，先确认修复目标和合法features。修复后审阅diff，核实所有权、错误、平台和features语义，重新执行受影响检查。clippy-driver用于lint，不是生产rustc替代品，产物可能不按预期优化。
6. 总结命令、工具链、包/features/target、相关测试数量和结果；单列未验证范围。没有执行则说建议命令，不说通过。

代码改写另核对匹配版本/edition的Reference：move/绑定模式、临时值及守卫析构、控制流边界、整数溢出和条件编译。不要用`if cfg!(...)`隐藏不存在的API；cfg!不是移除代码。语言语义、API合约和lint风格建议分开；Reference不规定优化策略，不用它证明迭代器更快或release溢出一定环绕。

## 快速参考

| 检查 | 能提供的证据 | 不能推出 |
| --- | --- | --- |
| fmt --check | 格式符合当前formatter/config | 能编译或行为正确 |
| cargo check | 所选配置通过编译检查 | 完整链接/运行行为正确 |
| cargo test | 已执行用例通过 | 所有输入、平台和features正确 |
| cargo clippy | 当前lint与配置的静态建议 | MSRV、线程安全业务逻辑或性能全面证明 |

### Clippy 分类与处理

| 类别 | stable文档默认等级 | 处理起点 |
| --- | --- | --- |
| correctness | deny | 优先核实错误/无效代码并修复 |
| suspicious | warn | 核对是否误用及真实意图 |
| style / complexity | warn | 评估可读性与简化，不机械改写 |
| perf | warn | 核对建议适用条件，不把lint当性能实测 |
| pedantic | allow | 项目选择启用，允许有依据的局部例外 |
| restriction | allow | 逐条选用，**不要整组启用**，可能互相矛盾且拒绝合理代码 |
| nursery | allow | 尚在开发，按安装版本评估 |
| cargo | allow | manifest相关检查，按项目需要选用 |

`clippy::all`包含默认开启的correctness/suspicious/style/complexity/perf，默认等级混合deny/warn；不是pedantic/restriction/nursery/cargo的总开关。类别与lint可能随版本变化，核对项目安装版本；官方入口链接到master lint清单也不证明该lint已在本地stable提供。

### 配置与范围

- lint等级放在源代码属性、`cargo clippy -- -A/-W/-D clippy::<lint>`，或实际Cargo支持的`[lints.clippy]`。`clippy.toml` / `.clippy.toml`配置lint行为参数，不用于声明warn/deny等级；不把配置键当稳定跨版本API。
- 配置搜索起点按首个已定义的`CLIPPY_CONF_DIR`、`CARGO_MANIFEST_DIR`、当前目录选择，再向父目录查找。检查是否加载了预期文件，不凭工作目录猜配置。
- MSRV沿用项目rust-version和实际Clippy支持的msrv配置；必要时查看覆盖优先级。不要给普通stable项目加入文档示例中的不稳定`custom_inner_attributes` / `clippy::msrv`属性。
- `-p`选包但仍可能lint workspace/path依赖；只lint所选包用实际支持的`cargo clippy -p <包> -- --no-deps`。此选项抑制依赖lint，不免除编译依赖。
- CI需要禁止所有警告时先遵守既有策略；实际Cargo支持`build.warnings`时可用`CARGO_BUILD_WARNINGS=deny cargo clippy`。所查stable文档标明该方式从Cargo1.97起推荐；旧版本可用`cargo clippy -- -D warnings`，可能影响构建缓存。两种均涉及rustc警告，不只是Clippy。
- 不为本次任务无条件增加deny策略；历史无关警告与新诊断分开报告。CI本就deny则照执行，不擅自弱化规则。不为新配置选项升级项目工具链。

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
