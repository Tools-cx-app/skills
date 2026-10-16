---
name: rust-async
description: Use when Rust work involves async functions, await, futures, tasks, streams, async concurrency, runtimes, or blocking work in asynchronous code.
---

# Rust 异步

## 适用

用于 Book 第17章的 future、async/await、任务、并发 future 和 stream。Rust语言提供异步语法，运行时、执行器和I/O能力由具体生态提供。

## 步骤

1. 先说明调用方需要的future输出、取消行为、并发度和运行时边界。
2. 区分创建future、轮询future、生成任务和等待结果；不把`async fn`调用当作立即执行。
3. 并发等待独立future，顺序依赖用`await`串联；阻塞工作移出异步执行器。
4. 核对跨await保存的借用、`Send`要求、错误传播、取消和资源释放。
5. 以项目已选runtime和feature验证；不从Book示例推导某个runtime的API。

## Future、Pin与Stream

`Future::poll`返回`Ready`或`Pending`；Pending后应通过waker安排后续轮询，不手写忙等，完成后不再次轮询，除非API明确允许。不同async块即使Output相同也是不同匿名类型；集合需要统一类型时考虑泛型组合或固定后的trait object。`Pin`限制被固定值的移动，不是“堆分配”的同义词；`Unpin`允许忽略该限制，不能为消除报错随意实现。Stream按次异步产生值，检查具体crate的Stream/StreamExt、结束和超时合约；Book的trpl是教学辅助，不要求项目采用它。

## 示例

```rust
async fn add(a: u32, b: u32) -> u32 { a + b }

fn main() {
    let future = add(2, 3);
    drop(future);
}
```

## 误区

- async函数返回的future惰性推进；创建任务可能立即调度，丢弃任务句柄是否取消任务由runtime决定。
- 并发不等于并行；runtime线程模型和任务调度决定实际执行。
- 跨`await`的值可能要求更严格的生命周期或`Send`，按调用上下文核对。

## 来源

[Book第17章](https://doc.rust-lang.org/book/ch17-00-async-await.html)、[async语法Reference](https://doc.rust-lang.org/reference/items/async.html)、[Future](https://doc.rust-lang.org/std/future/trait.Future.html)。
