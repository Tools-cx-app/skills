---
name: rust-errors
description: Use when Rust APIs must distinguish missing values from failures, propagate Result or Option, convert error types, retain error context, or decide whether unwrap, expect or panic is appropriate.
---

# Rust 错误与缺失值

## 适用场景

用户输入、配置、文件、网络等失败需要调用方处理；或现有代码吞掉错误、重复转换、滥用 panic。先定义失败语义，再选择类型；不默认新增错误处理依赖。

## 操作步骤

1. 核实项目 rustc/cargo、MSRV、edition 和已有错误约定。不固定工具链、不默认 nightly；新方法先核实稳定版本。旧版本可用 match/map_err 替代较新便捷方法。
2. 列出成功、缺失、损坏和外部失败：`Option<T>` 表示可接受的缺失；`Result<T,E>` 表示可解释失败；两者共存用 `Result<Option<T>,E>`。明确空白、文件不存在、编码错误与值范围的业务含义。
3. 在信任边界验证输入，保留 I/O/解析等原因；`.ok()` 仅在故意放弃错误信息时使用。不要将所有错误转换为 None 或默认值。
4. `?` 要求兼容返回类型；Result错误通过 From 转换，或用 map_err 显式映射；Option转Result使用 ok_or/ok_or_else，Result/Option不可无条件混用。错误上下文记录操作和必要位置，保留 source；日志/消息避免泄露敏感输入。
5. 复用已安装错误库和现有错误类型。库需要调用方匹配时用明确枚举；应用边界可采用现有统一错误类型。只有调用方需要标准Error接口时实现 Display/Error/source；不用为了一个错误加框架。
6. 测试有效、缺失、损坏、范围边界和外部失败；让调用方决定退出、重试或展示。`unwrap/expect` 适合测试或已证明的不变量；启动失败即退出必须是明确策略，不能冒充可恢复错误接口。

### 按 Reference 核对控制流

- Result的?在Ok时取值，Err时提前返回并转换错误；Option的?在None时提前返回None。位于闭包/async块时作用于该闭包/块的返回边界，不是任意外层函数；返回类型不兼容就显式match/转换，不把?当捕获机制。
- 不给stable项目实现自定义Try/FromResidual来扩展?；这些trait的稳定性单独核对，不由最新Reference中展示的语义推断所有历史版本均支持。
- panic策略区分unwind与abort：unwind会展开Rust栈并执行沿途活跃值的析构，abort不提供该清理或恢复过程；catch_unwind仅用于其API允许的展开情形，不能捕获abort，不能替代输入错误Result。析构不是跨所有终止路径的资源持久化保证。

## 快速参考

| 语义 | 形式 |
| --- | --- |
| 未找到是正常结果 | Option<T> |
| 查询失败需保留原因 | Result<T,E> |
| 查询可能成功但没有值 | Result<Option<T>,E> |
| 当前层添加操作上下文 | map_err 或既有库上下文接口 |
| 编程不变量被破坏 | 按项目约定 expect/panic，解释不变量 |

## 最小示例

空白代表未设置；0是否有效由业务另定，本例允许。通用的 match、map 和 parse，不依赖近期 API。

```rust
use std::num::ParseIntError;

fn parse_port(text: &str) -> Result<Option<u16>, ParseIntError> {
    let text = text.trim();
    if text.is_empty() {
        Ok(None)
    } else {
        text.parse::<u16>().map(Some)
    }
}

fn main() {
    assert_eq!(parse_port(" 8080 ").unwrap(), Some(8080));
    assert_eq!(parse_port(" \n ").unwrap(), None);
    assert!(parse_port("invalid").is_err());
    assert!(parse_port("65536").is_err());
    assert_eq!(parse_port("0").unwrap(), Some(0));
}
```

读取层另保留 I/O 和解析变体，不用 `.ok()` 抹平；read_to_string 的无效UTF-8归为I/O InvalidData，业务需另归类时显式处理。读取API若不支持项目MSRV，可复用项目已有Read读取方式。

## 常见误区

- `?` 不是捕获错误，而是传播；无依据改为 panic 会改变服务故障行为。
- `Option` 不等于“任何失败”；错误字符串不等于可匹配的错误分类。
- `From` 应表达适当转换，增加上下文用 map_err；不能因代码短就丢 source。
- 标准库内部 panic 或不稳定 Try trait 实现不是业务错误策略；no_std 与 std 的 Error 可用版本分别查询。

## 来源

[合约与源码依据](references/sources.md)；版本/API 核实时使用 rust-docs。未加载该技能时直接查目标版本官方API文档与稳定性标记，不能以当前工具链编译代替MSRV验证。
