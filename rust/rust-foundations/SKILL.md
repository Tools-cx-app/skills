---
name: rust-foundations
description: Use when Rust work involves variables, mutability, types, functions, control flow, structs, enums, pattern matching, methods, expressions, or basic syntax.
---

# Rust 基础语言

## 适用

用于从需求映射到 Rust 基础语法和数据模型。以 Rust Book 第3、5、6、19章为教学主线；精确语义和版本差异另查 Reference。

## 步骤

1. 先确定值的类型、所有权需求、可变性和生命周期范围。
2. 用结构体表达相关字段，用枚举表达互斥状态；让方法接收者表达读、写或消费。
3. 用 `match` 处理完整状态，用 `if let`/`let else` 只在剩余分支明确时简化。
4. 检查模式是否可反驳、表达式是否返回值、整数类型和转换是否明确。
5. 再根据实际edition核对模式、数组、保留关键字和语法差异。

## 语法决策

- 不变绑定、`mut`、常量与遮蔽分别表达不可重新赋值、可修改、编译期常量和重新绑定；不要为方便统一加mut。
- 函数参数声明类型；语句与表达式区分分号，尾表达式决定块结果。`if`分支类型需协调，`loop`可通过带值break产生结果，while/for用于条件/迭代。
- struct更新语法可能移动未显式指定的非Copy字段；`&self`、`&mut self`、`self`分别表达共享读、独占改和消费，关联函数不一定有self。
- `Option<T>`不是隐式null，match穷尽枚举；`if let`关注单一分支，`let else`失败分支必须发散。解构、守卫、`@`绑定与`_`忽略用途不同；`_name`仍绑定并可能拥有值。

## 示例

```rust
enum Command { Add(i32, i32), Quit }

fn run(command: Command) -> Option<i32> {
    match command {
        Command::Add(a, b) => Some(a + b),
        Command::Quit => None,
    }
}

fn main() {
    assert_eq!(run(Command::Add(2, 3)), Some(5));
    assert_eq!(run(Command::Quit), None);
}
```

## 误区

- `mut` 只改变绑定或借用的可变性，不自动创建 `&mut`。
- `match` 不是只处理“常见情况”；枚举分支必须有明确覆盖。
- `as` 不是通用安全转换；范围和截断必须按目标类型核对。

## 来源

[Rust Book第3章](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)、[第5章](https://doc.rust-lang.org/book/ch05-00-structs.html)、[第6章](https://doc.rust-lang.org/book/ch06-00-enums.html)、[第19章](https://doc.rust-lang.org/book/ch19-00-patterns.html)、[Reference](https://doc.rust-lang.org/stable/reference/)。
