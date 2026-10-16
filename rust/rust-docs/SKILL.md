---
name: rust-docs
description: Use when Rust work requires checking Book explanations, language rules, standard-library APIs, exact crate versions, Cargo behavior, feature gates, editions, or offline documentation.
---

# Rust 文档查询

## 适用

用于需要权威依据的 Rust 判断。Book用于教学主线，Reference用于语言语义，rustdoc用于API，Cargo/Clippy文档用于工具行为。

## 步骤

1. 先确认rustc/cargo、MSRV、edition、target、crate精确版本和features。
2. 按问题选择来源：Book、Reference、Edition Guide、标准库rustdoc、docs.rs、Cargo Book或Clippy Book。
3. 打开具体条目核对签名、稳定版本、feature、cfg、Panics/Errors/Safety和示例；搜索摘要不算证据。
4. 网络不可用时查本地工具链文档、源码或缓存，并标明未核实项；不自动升级或安装。
5. 输出来源、版本配置、合约、结论和限制；滚动stable不能证明历史MSRV行为。

## 示例

查询“某个API在MSRV 1.70是否可用”时，先查看项目实际版本和目标target，再打开`https://doc.rust-lang.org/1.70.0/std/`的具体API条目，核对稳定版本和cfg；不能只看当前stable页面。

## 误区

- Book的简化说明不替代Reference和API合约。
- docs.rs展示的feature可能比项目启用的更多。
- 类型稳定不代表关联方法、trait实现或const用法在目标版本稳定。
- 页面404或搜索不到不证明API不存在，可能是版本、feature或target差异。

## 来源

[Rust Book](https://doc.rust-lang.org/book/)、[Reference](https://doc.rust-lang.org/stable/reference/)、[标准库](https://doc.rust-lang.org/std/)、[Cargo Book](https://doc.rust-lang.org/cargo/)、[Clippy Book](https://doc.rust-lang.org/stable/clippy/)。
