---
name: rust-docs
description: Use when Rust answers require authoritative API or language documentation, exact crate-version docs, feature gates, stabilization or MSRV checks, Cargo rules, rustdoc searches, or an offline fallback for unavailable documentation.
---

# Rust 文档查询

## 适用场景

核实API、trait约束、语言规则、features、稳定版本和平台限制。找到页面不等于API适用于项目；回答必须匹配版本与构建配置。

## 操作步骤

1. 确认问题中的完整路径/符号、实际rustc/cargo、MSRV、edition、target、crate精确版本与features。读项目工具chain/manifest/lock；必要时用实际支持的metadata/tree。edition不是编译器版本；声明版本要求不是已解析版本。用户明确给出已锁版本时按该事实查询，不无依据改成latest。
2. 按表选择官方来源。标准库以目标Rust版本文档为准，URL通常为 `https://doc.rust-lang.org/<rust-version>/std/`，no_std另看core/alloc；版本缺失则核实当前环境或给条件结论。第三方用 `https://docs.rs/<package>/<exact-version>/<crate>/`；package可能含连字符，crate模块常用下划线，确认入口而非猜路径。
3. 使用rustdoc完整路径/名称检索如 `Vec::with_capacity`；不知名称时可尝试类型签名检索如 `usize -> Vec`。结果必须打开条目检查，模糊匹配和近似签名不是证明。旧rustdoc不支持相同搜索语法时退回模块索引/页面文本；网页404时找当前入口，不反复请求错误路径。
4. 检查签名、trait/关联类型、稳定since、const稳定版本、deprecated、nightly gates、features、target/cfg、Panics/Errors/Safety与示例。仅类型稳定不证明所用方法/trait实现/const用法稳定。docs.rs可由metadata选择features与target，cfg(doc)/文档专用cfg也可能扩大展示；不能假设总开all-features，也不能把其nightly构建成功视为项目MSRV成功。
5. 页面缺项/矛盾时查同版本Source、Cargo.toml及cfg/re-export；内部实现只能解释行为，不能替代公开合约。lock不记录最终features，resolver/host/target/dev上下文分别确认。语言规则查Reference，入门解释查Book，edition差异查Edition Guide，Cargo行为查匹配Cargo Book/本机help；滚动语言文档不自动证明历史版本行为，Reference也不是覆盖所有细节的完整形式化规范。
6. 无网络优先读取已安装目标工具链文档、本地已有target/doc或缓存的精确版本源码；已有文档先核实是否陈旧及生成配置，不存在则明确“未核实”。需要生成文档时先确认选项和项目features；cargo doc会构建文档、执行构建脚本并可能联网，不是纯查询；需限制Cargo联网/不改lock且支持时用frozen，不自动回退。frozen不是只读模式或网络沙箱，不能约束build.rs自行联网。不要为查询默认安装/升级工具链或开启全部features。
7. 给出来源、版本/配置、合约要点、结论与未确定项。可用项目工具链编译最小调用补验证；不要声称未访问页面已查证或未运行编译已通过。查询不足时仍可解释方法，但结论保持条件性。

## 快速来源表

| 问题 | 首选 |
| --- | --- |
| std/core/alloc类型、方法、trait | 目标Rust版本API rustdoc |
| 第三方crate API/features | 精确版本docs.rs、发布源码/manifest |
| 语言语义/语法 | Rust Reference |
| 教学解释 | The Rust Book |
| edition行为差异 | Edition Guide |
| manifest/resolver/命令 | 对应Cargo Book、实际cargo help |
| nightly/unstable | 对应版本Unstable Book/跟踪issue，不默认可用 |

## 最小示例

输入：“MSRV1.70，edition2021，tokio已锁1.28.2且只请求rt，能用tokio::net吗？”

输出结构：
- **来源**：精确1.28.2文档/源码条目链接；未访问时明确“待核实链接”，不编造摘录。
- **版本/配置**：Rust1.70、edition2021、tokio1.28.2、实际target；rt请求与最终联合features分别确认。
- **合约**：检查该版本net模块及具体API的feature/cfg；不由latest页面或docs.rs显示推断本项目可用。
- **结论**：若已核实需要net而最终未启用，则当前配置不可用；其他依赖可能启用net，需查实际图。
- **限制**：文档未访问或图未解析时不宣称确定可用；不自动新增feature或升级依赖。

## 常见误区

- 最新stable文档含有比MSRV新API；nightly文档/最新crate文档不适用所有项目。
- “网页找不到”推导API不存在；隐藏项可能源自feature、target、版本或发布文档构建失败。
- 只引用搜索摘要，不读签名/稳定性/错误条件；用当前源码实现证明历史行为。
- 标准库与Cargo版本关联但不是同一个字段；rust-version声明不等于现场实际版本。

## 来源

[rustdoc、人类指南与docs.rs依据](references/sources.md)。其他五项技能只在需要核实规则/API时使用本流程，不需要无条件互相加载。
