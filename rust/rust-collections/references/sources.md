# 来源与证据边界

原创归纳。rust-lang/rust 固定修订 `28221559263a3976766cf305940e80e30cf9ba8a`，MIT OR Apache-2.0。

- [std collections 指导](https://doc.rust-lang.org/std/collections/index.html)，[对应源码](https://github.com/rust-lang/rust/blob/28221559263a3976766cf305940e80e30cf9ba8a/library/std/src/collections/mod.rs)：人类编写的容器选择、复杂度和Entry指导。
- [Vec合约](https://doc.rust-lang.org/std/vec/struct.Vec.html)，[vec/mod.rs](https://github.com/rust-lang/rust/blob/28221559263a3976766cf305940e80e30cf9ba8a/library/alloc/src/vec/mod.rs)：Capacity/Guarantees，with_capacity，增长策略不保证。vec内存布局与内部实现不作为unsafe应用模板。
- [BTreeMap合约](https://doc.rust-lang.org/std/collections/struct.BTreeMap.html)，[btree/map.rs](https://github.com/rust-lang/rust/blob/28221559263a3976766cf305940e80e30cf9ba8a/library/alloc/src/collections/btree/map.rs)：按Ord排序迭代和Entry API。
- [HashMap合约](https://doc.rust-lang.org/std/collections/struct.HashMap.html)：任意迭代顺序、哈希安全边界。当前哈希算法不能保证跨版本固定。
- [Iterator](https://doc.rust-lang.org/std/iter/trait.Iterator.html)：适配器与消耗方法；[数组IntoIterator的edition差异](https://doc.rust-lang.org/edition-guide/rust-2021/IntoIterator-for-arrays.html)。

“先用标准容器、性能先测量”是条件性建议；具体版本下的分配次数、向量增长倍数和哈希桶布局是实现细节。示例usize上界来自输入为已存在切片的前提，不推广到累计多个批次或无界流。

2026-10-05读取[stable Reference循环](https://doc.rust-lang.org/stable/reference/expressions/loop-expr.html)：for/IntoIterator/Iterator展开与不可反驳模式；[运算符](https://doc.rust-lang.org/stable/reference/expressions/operator-expr.html)：整数溢出与检查例外；[介绍](https://doc.rust-lang.org/stable/reference/index.html)：可观察行为及优化范围。语言协议不保证性能或容器容量，后者须查对应API。
