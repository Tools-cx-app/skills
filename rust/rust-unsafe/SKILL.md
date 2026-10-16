---
name: rust-unsafe
description: Use when Rust work involves unsafe blocks, raw pointers, FFI, UnsafeCell, unsafe traits, macros, advanced types, or reviewing a safety invariant.
---

# Rust 高级与 Unsafe

## 适用

用于 Book 第20章和附录D中需要明确安全边界的工作。默认先寻找安全抽象；无法避免unsafe时，把不变量写成可审阅的契约。

## 步骤

1. 先判断安全Rust、已有标准库或成熟crate是否能表达需求。
2. 每个unsafe操作前写出前置条件、别名规则、初始化、布局、线程和生命周期不变量。
3. 把unsafe限制在最小边界，向外提供安全API；检查所有调用路径是否维护不变量。
4. FFI核对ABI、所有权、空指针、错误码、线程和库生命周期；不凭函数名猜合约。
5. 对裸指针、`UnsafeCell`、unsafe trait和宏展开分别检查；用Miri或目标工具链支持的检查补证据。

## 高级边界

Book区分解引用裸指针、调用unsafe函数、访问可变static、实现unsafe trait和访问union字段；unsafe块仍执行借用检查，不能把所有操作归为“不检查”。用安全函数包装unsafe操作时，安全调用者的所有合法输入都必须维护不变量。FFI的`extern` ABI、unsafe extern和属性要求随edition核对。

宏不自动包含unsafe。`macro_rules!`按token模式匹配/重复展开；过程宏分derive、attribute和function-like，定义在独立的proc-macro crate，接收/返回TokenStream。选择宏是为了生成语法或可变形态，不是替代普通函数；核对作用域、路径卫生、表达式求值次数和错误诊断。普通高级trait/type设计使用rust-types，不能因放在第20章就要求unsafe。

## 示例

```rust
fn first(values: &[u8]) -> Option<u8> {
    values.first().copied()
}

fn main() {
    assert_eq!(first(&[7]), Some(7));
}
```

## 误区

- `unsafe`只关闭部分编译器检查，不代表代码自动正确或更快。
- `transmute`、裸指针和FFI不能用“布局看起来一样”证明安全。
- `UnsafeCell`允许内部可变性，但不取消`&mut`独占和线程同步要求。
- 宏可以生成危险代码；审查展开后的语义和调用方输入。

## 来源

[Book第20章](https://doc.rust-lang.org/book/ch20-00-advanced-features.html)、[Unsafe Rust](https://doc.rust-lang.org/book/ch20-01-unsafe-rust.html)、[Reference unsafe](https://doc.rust-lang.org/stable/reference/unsafe-keyword.html)。
