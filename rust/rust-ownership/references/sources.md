# 来源与证据边界

本技能是原创归纳，不复制上游注释。源码基于 rust-lang/rust 修订 `28221559263a3976766cf305940e80e30cf9ba8a`（MIT OR Apache-2.0）；链接指向固定修订，文档站链接可能更新。

| 结论 | 证据类别 | 阅读来源 |
| --- | --- | --- |
| 借用不接管所有权；引用有效性与独占借用约束 | 语言规则的教学解释 | [Book borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html)；严谨规则另查 [Reference](https://doc.rust-lang.org/reference/types/pointer.html) |
| Rc 共享分配且非线程安全 | 公开API合约及实现 | [rcs/rc.rs](https://github.com/rust-lang/rust/blob/28221559263a3976766cf305940e80e30cf9ba8a/library/alloc/src/rcs/rc.rs)，模块说明与 !Send/!Sync 实现 |
| Arc 不使内部 RefCell 线程安全 | 公开API合约 | [rcs/arc.rs](https://github.com/rust-lang/rust/blob/28221559263a3976766cf305940e80e30cf9ba8a/library/alloc/src/rcs/arc.rs)，Thread Safety；[Book shared state](https://doc.rust-lang.org/book/ch16-03-shared-state.html) |
| Box 是独占堆所有权，可用于递归大小 | 公开API合约 | [boxed.rs](https://github.com/rust-lang/rust/blob/28221559263a3976766cf305940e80e30cf9ba8a/library/alloc/src/boxed.rs)，Examples |
| scope 可以借用非static数据，1.63稳定，spawn仍需Send | 公开API及稳定属性 | [thread/scoped.rs](https://github.com/rust-lang/rust/blob/28221559263a3976766cf305940e80e30cf9ba8a/library/std/src/thread/scoped.rs)，Scope::spawn；[scope API](https://doc.rust-lang.org/std/thread/fn.scope.html) |

锁选择和接口优先借用属于条件性开发建议；Rc/Arc 性能差异不能替代对实际工作负载的测量。标准库内部布局和具体原子内存序仅用于理解实现，不构成应用代码必须遵循的实现模板。

补充公开合约：[spawn](https://doc.rust-lang.org/std/thread/fn.spawn.html)、[RefCell](https://doc.rust-lang.org/std/cell/struct.RefCell.html)、[Mutex](https://doc.rust-lang.org/std/sync/struct.Mutex.html)、[Clone](https://doc.rust-lang.org/std/clone/trait.Clone.html)。查询目标版本的方法见 rust-docs 技能；该技能不可用时直接访问目标版本官方 API 页面并核对稳定版本。
