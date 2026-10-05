---
name: rust-collections
description: Use when Rust code needs collection selection, ordered or keyed output, frequency counts, Entry updates, iterator ownership decisions, capacity planning, or investigation of unnecessary allocation and cloning.
---

# Rust 集合、迭代与分配

## 适用场景

选择容器、统计和排序、调整迭代所有权或减少已确认的分配。先满足顺序、重复、访问和所有权语义，再谈性能；不用实现细节冒充公开保证。

## 操作步骤

1. 核实项目 rustc/cargo、edition、MSRV 和数据来源；不默认 nightly 或新增集合依赖。新方法核对稳定版本，旧版本可用 match、entry 和显式循环。
2. 确认输出顺序、重复键处理、更新频率、是否仅末尾追加。选下表的标准容器；现有容器加一次排序已满足需求时不强制重写。
3. 只读用 iter/借用，原地修改用 iter_mut，接管元素用 into_iter；方法接收者决定移动还是借用。数组按值IntoIterator要求Rust≥1.53；edition2018的数组.into_iter()保持借用兼容，按值用IntoIterator::into_iter(array)，借用明确用array.iter()。不同版本/edition不套用Vec规则。
4. Map更新用 entry 避免查找后再插入；持久存储键决定借用键是否活得足够久。无界流计数明确溢出策略，checked_add返回错误优于默默环绕；已知内存内输入的计数可利用总长度上界。无界流另定义标签基数/字节预算和快照或终止边界；检查整数溢出不解决内存无界。
5. 容量是预留空间，不是len：核实问的是 Vec 还是 HashMap，再查该类型合约。Vec::with_capacity(n) 至少n，非恰好n；零大小类型例外、增长倍数和分配器行为不能硬编码。未知长度先用new，不从不可信输入无界预分配。
6. 性能优化先测实际负载与目标构建；比较分配、拷贝、哈希/比较成本。循环和迭代器没有普遍快慢保证。需要可恢复分配失败时按容器查询项目版本的try_reserve等API；Vec的try_reserve不能用于BTreeMap，不假定所有分配都返回Result。

## 快速选择

| 需求 | 起点 |
| --- | --- |
| 顺序追加、栈、连续元素 | Vec |
| 两端队列 | VecDeque |
| 按键查询，无顺序要求 | HashMap |
| 按键升序遍历或范围查询 | BTreeMap |
| 去重，无值 | HashSet / BTreeSet（按排序需求） |
| 每次取最高优先级 | BinaryHeap |

HashMap不保证插入顺序；BTreeMap按键Ord遍历，不等于地区语言的自然排序。仅一批数据最终有序也可 Vec排序/聚合。输入已保证全局非递减且只末尾追加时，Vec<(标签,计数)>比较最后一组即可；可逐组输出时只保存当前组，无需Map。外部输入的排序前提需要验证。

## 最小示例

来自已驻留内存的切片，每个标签计数不超过切片len，因此usize递增有上界；无界流需要另用checked_add。

```rust
use std::collections::BTreeMap;

fn counts<'a>(tags: &[&'a str]) -> BTreeMap<&'a str, usize> {
    let mut result = BTreeMap::new();
    for &tag in tags {
        *result.entry(tag).or_insert(0) += 1;
    }
    result
}

fn main() {
    let result = counts(&["b", "a", "b"]);
    let ordered: Vec<_> = result.into_iter().collect();
    assert_eq!(ordered, vec![("a", 1), ("b", 2)]);
    assert!(counts(&[]).is_empty());
    let values: Vec<u8> = Vec::with_capacity(10);
    assert_eq!(values.len(), 0);
    assert!(values.capacity() >= 10);
}
```

## 常见误区

- 把HashMap容量文档拿来回答Vec，或把观察到的迭代顺序当保证。
- reserve参数是“额外元素数”，不要与总容量混淆；reserve_exact也不承诺底层分配恰好请求大小。
- 为collect先clone全部数据，或以“迭代器总快”为由重写可读循环。
- 更换哈希器、引入小向量或自写unsafe容器而没有性能证据；外部不可信键还需考虑碰撞攻击。

## 来源

[容器合约与源码依据](references/sources.md)。版本/API查询按 rust-docs；不可用时查目标版本标准库文档。
