---
name: rust-ownership
description: Use when Rust work involves ownership, moves, borrowing, references, slices, lifetimes, Box, Rc, RefCell, Drop, interior mutability, or shared data.
---

# Rust 所有权

## 适用

用于 Book 第4、15章和第16章共享状态部分。先用所有权表达资源关系，再考虑clone、引用计数或锁。

## 步骤

1. 标出每个值的拥有者、移动点、借用范围和析构点。
2. 只读参数优先借用；需要消费时按值接收；需要可变修改时使用独占可变借用。
3. 用切片表达连续数据视图，用生命周期表达输入引用之间的关系，不用标注制造寿命。
4. 递归大小或明确堆所有权才用`Box`；多所有者再选`Rc`/`Arc`，运行时借用检查再选`RefCell`。
5. 跨线程核对`Send`/`Sync`和同步协议；`Arc`不自动让内部值线程安全。
6. 部分移动、临时值和守卫析构按实际作用域检查；不要依赖猜测的语句末释放。

生命周期标注描述引用之间的约束，不创建或延长存储；返回借用应来自仍存活的输入，无法借用时返回拥有的数据。`Deref`支持智能指针解引用及有限的自动转换，`Drop`负责资源清理，提前清理用`std::mem::drop`而非显式调用drop方法。`Rc`强引用形成环可能泄漏，反向非拥有关系考虑`Weak`；内存泄漏并不因安全Rust而绝对消失。

## 示例

```rust
fn first_word(text: &str) -> &str {
    text.split_whitespace().next().unwrap_or("")
}

fn main() {
    let text = String::from("hello world");
    assert_eq!(first_word(&text), "hello");
}
```

## 误区

- 借用错误不应一律用clone掩盖；先修正接口的拥有关系。
- `Clone`不承诺深拷贝，`Copy`也不是任意复制的替代品。
- 实现`Drop`的值不能直接移出非Copy字段；需要替代值时使用明确API。
- `RefCell`把检查移到运行时，不会消除借用规则或数据竞争。

## 来源

[Book第4章](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)、[第15章](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)、[第16章](https://doc.rust-lang.org/book/ch16-00-concurrency.html)、[所有权Reference](https://doc.rust-lang.org/stable/reference/)。
