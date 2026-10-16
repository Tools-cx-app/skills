---
name: rust-concurrency
description: Use when Rust work involves threads, channels, shared state, Send, Sync, scoped work, thread pools, shutdown, or cross-thread ownership.
---

# Rust 并发

## 适用

用于 Book 第16章和第21章的线程、消息、共享状态与线程池场景。先明确数据流和停止条件，再选通信或共享状态。

## 步骤

1. 判断任务是转移数据、发送事件，还是多个线程共享同一状态。
2. 只发送一次的数据优先消息传递；需要共享状态时选择合适的锁或原子类型。
3. 核对闭包捕获、`Send`/`Sync`、线程生命周期和错误传播；不要只替换 `Rc` 为 `Arc`。
4. 设计线程退出、channel关闭、join、锁中毒和任务失败的行为。
5. 用受控输入测试并发结果；不要把一次运行通过当作没有竞态。

## 任务与关闭

`move`把捕获值移入线程闭包；普通spawn通常要求捕获满足`Send + 'static`，`'static`不表示线程永远运行。仅在作用域内借用时核对scoped thread支持。channel的发送转移值所有权，所有sender关闭后receiver才结束；有界channel还需考虑背压。

Book第21章线程池用Job闭包分发连接；实际服务应限定队列/线程资源，关闭时先停止接收、断开发送端，再join工作线程，避免receiver等待消息而主线程等待join。锁守卫先退出作用域再执行长任务；死锁不能由借用检查自动排除。

## 示例

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    let worker = thread::spawn(move || tx.send(2 + 3).unwrap());
    assert_eq!(rx.recv().unwrap(), 5);
    worker.join().unwrap();
}
```

## 误区

- `Arc<T>`只提供共享所有权，不让内部类型自动变成线程安全。
- `Mutex`保护访问，不自动解决死锁、长时间持锁或业务失败。
- channel关闭、线程panic和join失败必须有明确处理，不用无界等待掩盖退出问题。

## 来源

[Book第16章](https://doc.rust-lang.org/book/ch16-00-concurrency.html)、[最终项目](https://doc.rust-lang.org/book/ch21-00-final-project-a-web-server.html)、[Send和Sync](https://doc.rust-lang.org/book/ch16-04-extensible-concurrency-sync-and-send.html)。
