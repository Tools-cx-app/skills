---
name: rust-collections
description: Use when Rust work involves Vec, String, HashMap, collection choice, iteration, ownership during traversal, ordering, capacity, or allocation behavior.
---

# Rust 集合与迭代器

## 适用

用于 Book 第8章和第13章。先根据数据关系选容器，再根据所有权和访问方式选择迭代。

## 步骤

1. 明确元素数量、键值关系、顺序要求、查找方式和生命周期。
2. 连续可变序列用`Vec`，UTF-8文本用`String`/`&str`，键值查询用`HashMap`；需要排序或稳定顺序时另选合适容器。
3. 只读用`iter`，原地修改用`iter_mut`，消费集合用`into_iter`；检查`for`的借用或移动。
4. 预估容量时用`with_capacity`，不把当前增长策略当公开保证；大流量输入避免无界累积。
5. 迭代器适配器保持意图清晰；性能结论用目标构建和实际负载测量。
6. 计数和算术明确溢出策略，不能把release名称当作必然环绕保证。

下面的计数输入为已存在切片，每项最多计数切片长度，故usize足以容纳；连续累计批次或无界流不具备此前提。

## 示例

```rust
use std::collections::HashMap;

fn counts<'a>(words: &[&'a str]) -> HashMap<&'a str, usize> {
    let mut result = HashMap::new();
    for word in words {
        *result.entry(*word).or_insert(0) += 1;
    }
    result
}

fn main() {
    assert_eq!(counts(&["a", "a"]).get("a"), Some(&2));
}
```

## 误区

- `String`是UTF-8字节序列，不是可按整数索引的字符数组。
- `HashMap`迭代顺序和哈希算法不是跨版本固定输出。
- `for x in values`可能消费集合，`for x in &values`和`for x in &mut values`表达不同借用。
- 容量、分配次数和迭代器速度不要从实现细节推断。

## 来源

[Book第8章](https://doc.rust-lang.org/book/ch08-00-common-collections.html)、[第13章](https://doc.rust-lang.org/book/ch13-00-functional-features.html)、[std collections](https://doc.rust-lang.org/std/collections/)、[Iterator](https://doc.rust-lang.org/std/iter/)。
