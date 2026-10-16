---
name: rust-types
description: Use when Rust work involves generics, trait bounds, associated behavior, trait objects, lifetimes as contracts, closures, function pointers, or macro-facing type design.
---

# Rust 类型抽象

## 适用

用于选择泛型、trait、trait object、闭包或函数指针表达共享行为。以 Book 第10、13、18、20章为主线。

## 步骤

1. 先写调用方需要的行为和输入输出，不先设计抽象层。
2. 同一编译期类型集合优先泛型；运行时异构集合且需要动态分派时才用 trait object。
3. 把 trait bound 放在真正需要它的位置；关联类型用于每个实现一个自然结果类型的情况。
4. 生命周期只表达引用关系，不能用标注替代实际拥有或同步策略。
5. 闭包先判断捕获方式和调用次数，再选择 `Fn`、`FnMut` 或 `FnOnce`。
6. 使用宏前先确认普通函数、泛型或trait不能直接表达需求。

## 选择边界

- `impl Trait`参数是泛型约束的简写；两个独立的`impl Trait`参数不要求同一具体类型，需要相同时用同一个类型参数。返回位置`impl Trait`要求各返回分支为同一具体类型。
- 外部trait不能直接为外部类型实现；需要适配时考虑本地newtype，不把类型别名当新类型。关联类型、默认泛型参数、supertrait和完全限定语法分别用于输出类型、默认参数、行为前置条件和名称消歧。
- `dyn Trait`用于动态分派，检查当前版本的dyn兼容性和对象生命周期；泛型通常单态化。不要把“面向对象”直接翻译成继承层级，Book的状态模式也可用枚举或类型状态表达。
- `FnOnce`可消费捕获值，`FnMut`可修改捕获状态，`Fn`不需修改捕获状态；`move`改变捕获所有权，不自动决定闭包只能调用一次。函数指针`fn`与捕获环境的闭包不同。
- 类型别名只改名字；newtype有独立类型身份。`!`表示不返回的路径，DST通常通过指针/引用访问，`?Sized`用于放宽隐含Sized约束。

## 示例

```rust
fn largest<T: Ord + Copy>(items: &[T]) -> Option<T> {
    items.iter().copied().max()
}

fn main() {
    assert_eq!(largest(&[3, 1, 2]), Some(3));
    assert_eq!(largest::<i32>(&[]), None);
}
```

## 误区

- trait object 有对象安全和动态分派约束，不是泛型的无成本替代。
- `Clone`、`Copy`、`Send`、`Sync` 是不同契约，不因类型“简单”自动添加。
- 生命周期参数不会延长数据寿命。

## 来源

[Book第10章](https://doc.rust-lang.org/book/ch10-00-generics.html)、[第13章](https://doc.rust-lang.org/book/ch13-00-functional-features.html)、[第18章](https://doc.rust-lang.org/book/ch18-00-oop.html)、[高级特性](https://doc.rust-lang.org/book/ch20-00-advanced-features.html)、[Reference](https://doc.rust-lang.org/stable/reference/)。
