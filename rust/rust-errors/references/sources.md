# 来源与证据边界

原创归纳。rust-lang/rust 修订 `28221559263a3976766cf305940e80e30cf9ba8a`，源码许可 MIT OR Apache-2.0。当前文档中的便捷API必须另核对项目版本。

- [Book recoverable errors](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html)：?、From、unwrap/expect 的人类说明。
- [core/result.rs](https://github.com/rust-lang/rust/blob/28221559263a3976766cf305940e80e30cf9ba8a/library/core/src/result.rs)：公开Result合约，传播说明及 ok/map_err 方法。
- [core/option.rs](https://github.com/rust-lang/rust/blob/28221559263a3976766cf305940e80e30cf9ba8a/library/core/src/option.rs)：缺失值语义与 ?。
- [std Error](https://doc.rust-lang.org/std/error/trait.Error.html)：Display/Debug/source 合约；[std/error.rs](https://github.com/rust-lang/rust/blob/28221559263a3976766cf305940e80e30cf9ba8a/library/std/src/error.rs) 提供上下文和错误报告的人类说明。
- [fs::read_to_string](https://doc.rust-lang.org/std/fs/fn.read_to_string.html)：I/O及非UTF-8失败，稳定版本需查目标工具链。
- [stable Reference 运算符](https://doc.rust-lang.org/stable/reference/expressions/operator-expr.html)：?的Result/Option语义与Try稳定性；[panic](https://doc.rust-lang.org/stable/reference/panic.html)：unwind/abort及展开清理。2026-10-05已读取相关内容；具体catch_unwind约束仍查标准库API，不把panic转成普通输入错误策略。

Result<Option<T>,E> 的选型、业务范围与边界退出策略是条件性建议。源码枚举的当前布局、内部Try/FromResidual实现不用于承诺所有版本内存布局或要求业务实现不稳定trait。
