---
name: rust-ownership
description: Use when Rust code has move or borrow errors, unclear lifetimes, unnecessary clone calls, or decisions involving Box, Rc, Arc, RefCell, Send, Sync, shared state or scoped threads.
---

# Rust 所有权与借用

## 适用场景

处理 E0382、E0499、E0502、生命周期错误，或决定数据如何传递和共享。只读调用先借用；需要接管数据才移动；需要独立副本才克隆。

## 操作步骤

1. 阅读值的创建处、所有调用方和最后使用处。确认是否存储、跨线程、逃逸当前作用域；检查项目实际 rustc/cargo、edition、MSRV 和已有类型约定。不默认 nightly，不为使用某个建议而升级工具链。
2. 为每个使用者确定读取、修改、接管、共享四种需求。收窄借用作用域，必要时先计算再修改；生命周期标注描述关系，不会延长数据寿命。
3. 按下表选择最小形式。只读接口通常使用 `&str`、`&[T]`；需要持有数据的接口可接收 `String`、`Vec<T>`。不要为了统一接口强加泛型。
4. 跨线程检查整个捕获值的 `Send`/`Sync`；按值转交 T 需 Send，共享 &T 需 Sync；Arc<T> 的 Send/Sync 要求 T 同时 Send+Sync。RefCell<T> 可在 T: Send 时独占转交，但不是 Sync。遇到错误沿内部字段追踪，不能仅替换外层智能指针。
5. 用真实调用方编译验证；比较修改前后所有权、锁持有时间和错误处理。API 版本不确定时使用 rust-docs 查询。

### 按 Reference 排查语言规则

- 先区分位置表达式与值上下文：Copy类型按值使用会复制，否则合法位置可能被移动；不是所有读取都会clone。部分移动后可使用未移动字段，移出字段未重新初始化前不能整体使用原值；实现Drop的类型不能直接移出非Copy字段，复制Copy字段或留下替代值的取出另按API处理。
- 解构/匹配先确认绑定模式：按值可能move/copy，ref/ref mut绑定引用；mut是绑定可变性，不等于自动取得&mut。匹配引用时考虑match ergonomics；edition2024收紧隐式引用模式下显式mut/ref及引用模式的写法，不跨edition机械改写。
- 借用的有效使用范围与析构作用域分别分析。局部变量通常在所属drop scope退出时析构；临时值有独立作用域和延长规则，不能声称都在语句末尾析构。edition2024的if-let/块尾临时值作用域与旧edition不同；锁守卫/RefCell借用守卫遇到阻塞或借用问题时重点核对实际释放点。
- 共享引用通常不允许改变指向内容；内部可变性经UnsafeCell基础上的安全抽象实现，优先用Cell/RefCell/锁/原子API。内部可变性不取消&mut独占要求，不以unsafe绕过别名规则。

## 快速选择

| 需求 | 起点 | 条件 |
| --- | --- | --- |
| 当前调用只读/独占修改 | `&T` / `&mut T` | 数据活得足够久；内部可变性另有约束 |
| 按值接收 | Copy类型复制，否则移动 `T` | 移动不是深拷贝，也不调用Clone |
| 递归类型或独占堆所有权 | `Box<T>` | 不提供共享所有权 |
| 单线程共享所有权 | `Rc<T>` | `Rc` 非 Send/Sync；修改可按需求用 RefCell |
| 跨线程共享只读所有权 | `Arc<T>` | 内部 T 必须满足相应 Send/Sync 约束 |
| 跨线程共享修改 | `Arc<Mutex<T>>` 等 | 先确认必须共享；RwLock/atomic 需符合访问模式 |
| 线程在作用域内结束 | `thread::scope` 借用 | Rust ≥1.63；仍需 Send/Sync；不用强加 Arc |

MSRV 低于1.63时不要新增标准库 scoped threads：按需求用已确认版本及传递依赖支持项目MSRV的既有 scoped-thread 依赖，或用稳定的 `thread::spawn` 移动所有权；共享只读可用 Arc。普通函数借用不需要 scoped threads。普通 spawn 即使立即 join 仍要求捕获满足 'static；move/Arc不是局部借用的完全等价替代。确需跨线程局部借用且无既有依赖时，评估新增兼容依赖；禁止新增依赖又不能改变语义时报告约束冲突，不自行升级。

`Arc::clone` 共享同一分配；`String::clone` 创建独立字符串数据。独立副本有明确需求时克隆合理。只需在线程间转交一个 Vec 时直接移动，不加共享锁。

任意 T: Clone 不保证递归深拷贝，例如 Vec<Arc<T>> 克隆后仍共享 T。迁移已有 Rc 状态时确认旧持有者应继续共享还是取得快照；重新包装复制的数据不会自动共享原状态。

## 最小示例

Rust ≥1.63。作用域线程只读借用，线程失败在本例测试边界通过 expect 报告。

```rust
fn total_bytes(items: &[String]) -> usize {
    items.iter().map(|s| s.len()).sum()
}

fn main() {
    let items = vec![String::from("rust"), String::from("文")];
    std::thread::scope(|scope| {
        let worker = scope.spawn(|| total_bytes(&items));
        assert_eq!(worker.join().expect("test worker failed"), 7);
    });
    assert_eq!(items[0], "rust");
}
```

## 常见误区

- `Arc<RefCell<T>>` 不会自动线程安全；RefCell 的借用计数不是线程同步。
- 到处 `clone()` 掩盖所有权设计；但为了独立生命周期/独立可变副本克隆不是错误。
- `'static` 不等于永远运行，`move` 不保证捕获内容都满足 `'static`。
- 不以 unsafe、泄漏内存或扩大锁作用域绕过借用错误。锁中毒、死锁和线程失败按项目错误策略处理。
- 智能指针引用计数、分配布局等实现细节不是业务 API 设计依据；不照搬标准库内部不稳定技巧。

## 来源

[公开合约、源码与版本依据](references/sources.md)。语言行为以匹配版本/edition的stable Reference为依据；智能指针和线程API仍查标准库合约。
