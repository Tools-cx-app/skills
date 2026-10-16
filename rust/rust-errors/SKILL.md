---
name: rust-errors
description: Use when Rust work involves Option, Result, panic!, the question-mark operator, error conversion, CLI failures, validation, or recoverability decisions.
---

# Rust 错误处理

## 适用

用于 Book 第6、9、12章。先区分可恢复失败、不可恢复bug和边界退出，再选择返回类型或panic。

## 步骤

1. 列出每个失败来源、调用方能否恢复以及需要保留的上下文。
2. 缺失值用`Option`，可解释失败用`Result<T, E>`；错误类型保留足够的来源和边界信息。
3. 用`?`传播当前函数能处理的错误；在闭包或async块中确认它作用于该边界。
4. 在输入、文件、环境变量和外部命令边界把错误转成用户可理解的结果。
5. 只在违反不变量或无法合理恢复时panic；`unwrap`/`expect`必须有可说明的不变量。
6. 测试成功、缺失、损坏和外部失败路径，明确退出码和stderr行为。

借鉴Book第12章把配置解析、业务run和main分开：业务函数返回错误，main将诊断写stderr并决定退出码；正常结果写stdout以便管道使用。缺失与失败同时存在时考虑`Result<Option<T>, E>`；不要用`.ok()`无声丢掉需要解释的失败。对于固定示例/测试的unwrap，文档应明确其教学上下文，不把它机械复制到外部输入路径。

## 示例

```rust
fn parse_port(input: &str) -> Result<u16, String> {
    input.parse::<u16>().map_err(|_| format!("invalid port: {input}"))
}

fn main() {
    assert_eq!(parse_port("80").unwrap(), 80);
    assert!(parse_port("nope").is_err());
}
```

## 误区

- `Option`不是吞掉错误的方式；有失败原因时使用`Result`。
- `?`会提前返回，不会捕获、重试或记录错误；需要时显式转换和补充上下文。
- `panic=abort`不可依赖栈展开清理，也不能用`catch_unwind`恢复。

## 来源

[Book第9章](https://doc.rust-lang.org/book/ch09-00-error-handling.html)、[第12章](https://doc.rust-lang.org/book/ch12-00-an-io-project.html)、[Result](https://doc.rust-lang.org/std/result/)、[panic Reference](https://doc.rust-lang.org/stable/reference/panic.html)。
