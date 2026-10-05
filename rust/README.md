# Rust 日常开发 skills

七项中文技能，按场景加载。rustc/cargo版本通用：使用项目实际工具链、edition、MSRV和依赖配置；不默认nightly，不要求升级。新API/选项标明适用条件；源码修订只追溯依据，不是版本要求。

| 技能 | 触发场景 |
| --- | --- |
| [rust-ownership](rust-ownership/SKILL.md) | move/borrow、生命周期、clone、智能指针和线程共享 |
| [rust-errors](rust-errors/SKILL.md) | Option/Result、错误传播、上下文和panic边界 |
| [rust-collections](rust-collections/SKILL.md) | 集合选择、顺序、计数、迭代、容量和分配 |
| [rust-cargo](rust-cargo/SKILL.md) | 依赖、features、workspace/resolver、lock与构建 |
| [rust-quality](rust-quality/SKILL.md) | fmt、Clippy、测试、MSRV与自动修复审阅 |
| [rust-docs](rust-docs/SKILL.md) | 官方规则/API、精确版本docs.rs、feature和离线查询 |
| [rust-crates-first](rust-crates-first/SKILL.md) | 新功能先查crates.io；用户明确自写或已有实现足够时例外 |

每个技能自带references/sources.md：语言规则、API合约、条件建议与实现细节分开；不将内部unsafe或不稳定API作为日常开发模板。本包为源码及人类文档的原创归纳，无大段上游复制。

## OpenCode 加载

技能发现和技能调用是两个步骤。当前机器全局配置已注册本目录，并通过instructions加载[任务路由规则](skill-loading.md)。其他机器可将各技能目录复制到项目 `.opencode/skills/` 或全局 `~/.config/opencode/skills/`，或在现有配置追加以下路径（保留其他配置和已有instructions）：

```json
{
  "instructions": ["/home/tweaks/skills/rust/skill-loading.md"],
  "skills": {
    "paths": ["/home/tweaks/skills/rust"]
  }
}
```

复制部署时需要七个技能目录；若使用路由规则，还需复制skill-loading.md并将instructions改为实际绝对路径。tests/docs不是运行必需。修改加载配置或安装技能后退出并重启OpenCode，再检查技能列表及实际skill调用；仅列出技能不证明已调用。

## 本地检查

在本目录运行：

```sh
python3 tests/check.py
python3 tests/check.py rust-docs rust-cargo
```

检查frontmatter、名称、相对链接和章节，并用当前rustc编译/运行四个完整Rust示例。需要Python3及支持edition2021的rustc；这是检查器的要求，不是七项技能的最低工具链要求。所有权scoped示例另需Rust≥1.63。

该检查不是多版本CI，也不执行网络查询、Cargo示例或上游工具链测试。行为测试场景和实际证据见 [tests/scenarios.md](tests/scenarios.md) 与 [tests/results.md](tests/results.md)。未运行的Rust/Cargo版本不宣称支持已验证。
