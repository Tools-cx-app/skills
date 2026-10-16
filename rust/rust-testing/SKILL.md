---
name: rust-testing
description: Use when Rust work involves unit tests, integration tests, doctests, test organization, test commands, regression tests, CLI behavior, or test-driven development.
---

# Rust 测试

## 适用

用于设计和验证 Rust 行为。以 Book 第11、12章和附录D为主线。

## 步骤

1. 先写一个能观察需求或回归的最小测试；错误修复先确认它会失败。
2. 单元测试放在模块附近，集成测试验证公开接口，文档测试验证用户调用方式。
3. 分离正常、边界、失败和外部环境场景；不要只测试实现细节或mock自身行为。
   `tests/`下每个顶层Rust文件是独立crate，只能使用公开API；共享辅助模块可放在`tests/common/mod.rs`，避免把它作为空测试目标。二进制项目将可测逻辑提取到库，main负责参数、输出和退出。
4. 按实际包、target、feature和工具链运行；记录命令、用例数量和未覆盖范围。
5. 测试通过后审阅改动，确认没有因测试便利扩大公开API或绕过错误处理。

## 示例

```rust
fn classify(value: i32) -> &'static str {
    if value < 0 { "negative" } else { "non-negative" }
}

#[cfg(test)]
mod tests {
    use super::classify;
    #[test]
    fn classifies_zero_without_special_case() {
        assert_eq!(classify(0), "non-negative");
    }
}

fn main() { assert_eq!(classify(-1), "negative"); }
```

## 误区

- `cargo test`只证明已执行的测试通过，不证明所有feature、平台或输入正确。
- 测试后补用例不能证明用例曾捕获缺陷；回归测试应先观察失败。
- doctest、集成测试和单元测试有不同可见性，不互相替代。

## 来源

[Book第11章](https://doc.rust-lang.org/book/ch11-00-testing.html)、[第12章](https://doc.rust-lang.org/book/ch12-00-an-io-project.html)、[附录D](https://doc.rust-lang.org/book/appendix-04-useful-development-tools.html)、[Cargo test](https://doc.rust-lang.org/cargo/commands/cargo-test.html)。
