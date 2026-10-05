# Reference skill application scenarios

新增rust-crates-first为行为优先技能，见末节；其压力场景另外验证规则与用户例外。

## stable Reference代码规则复测

读取相关技能后分别判断：Copy/非Copy按值与clone，部分移动及Drop字段，mut与ref/match ergonomics，临时值/锁守卫是否总语句末释放及edition2024差异；闭包中?返回边界与stable自定义Try；panic=abort是否catch_unwind并执行析构；for values/&values/&mut values是否消耗容器、表达式是否每轮求值、是否保证迭代器更快；release算术是否必然环绕、MIN/-1例外；if cfg!(feature)是否隐藏缺失API；Reference是否是标准库/Cargo/优化/风格规范，历史版本与edition如何匹配。通过要求解释来源边界，不能把最新stable语法强推旧版。

每组给测试子代理：只解释，不编辑文件；作出选择并说明依据。第一轮不得读取当前rust技能目录或相应技能；复测读指定技能后回答原输入。版本信息不足时需指出影响，不能臆定 stable/MSRV。人工评分检验语义，不以关键词命中代替理解。

## rust-ownership

输入：服务把 Rc<RefCell<Vec<String>>> 交给线程，负责人建议只把 Rc 改为 Arc 就够了；配置字符串只需读取，提出到处 clone 来绕过借用问题。另外 scoped thread 是否必须 Arc？项目工具链未知。请提出最小选择，并区分类型约束与运行时锁。

通过：Arc 不使 RefCell Sync；共享只读可借用/Arc<T>，共享可变按实际同步需求选 Mutex/RwLock；避免 blanket clone；scoped thread 可借用，但仍需 Send/Sync；不能把新 API 自动用于未知 MSRV。反例：确需独立所有权时 clone 合理。

## rust-errors

输入：读取用户指定的端口文件，空文件表示未设置；损坏内容应报错。用 read_to_string(...).ok()?.trim().parse().ok() 可以吗？API 要向调用者区分 I/O、解析和未设置，负责人希望全部 unwrap 保持简洁。无需新的错误依赖。未知 MSRV。

通过：Result<Option<u16>, E> 保留三态；.ok() 会丢失信息；? 需要 From/兼容错误返回类型；预期外部输入失败不 panic；示例/方案覆盖 I/O、空值、解析错误、端口范围。反例：已证明内部不变量可 expect；不强制新增 thiserror/anyhow。

## rust-collections

输入：统计标签次数并按标签升序输出。负责人说 HashMap 迭代就是插入顺序，Vec::with_capacity(10) 保证恰好分配10，迭代器必然比循环快，因此全改迭代器。输入长度未知、项目 MSRV 未知。选择最小结构与更新方式。

通过：BTreeMap 或 HashMap+排序；无 HashMap 顺序保证；capacity 至少请求值、不要声称固定增长因子；Entry 计数；性能需测量；只读迭代不强制 clone；安全检查整数溢出条件。反例：仅追加有序数据可 Vec，无需 Map。

## rust-cargo

输入：workspace 有多个 crate，某库启用依赖的 foo feature、另一个启用 bar feature。能认为 default-features=false 会在整个图里禁用 defaults 吗？workspace 根是虚拟 manifest，成员 edition=2024，rust-version=1.85。发布构建 cargo build --locked 是否等于断网？负责人希望只测 --all-features 就能验证互斥 backend。给出核实步骤，不更改依赖。

通过：features 按 resolver 规则联合，default-features=false 非全局 veto；虚拟 workspace resolver 要显式选择、不由成员 edition 推导；locked 可联网、offline/frozen 区别；1.85/2024 与 resolver3 兼容条件；互斥 features 不适合仅 all-features；列出目标 feature 矩阵和只读检查命令。

## rust-quality

输入：格式检查和 cargo check 已过，无测试输出，可以宣布行为正确吗？CI 仅 stable，MSRV=1.70。负责人要 cargo clippy --all-targets --all-features --fix --allow-dirty 并自动升级 lint 推荐的新 API。仓库有互斥 backend features。提出最小可靠检查顺序，区分检查结果和未验证范围。

通过：fmt/check 不证明运行行为；针对受影响行为测试；Clippy 与 rust-version/MSRV；all-features 有前提；不无条件 allow-dirty/自动升级；修复后审阅diff重测；不强制 unrelated lint 清零。反例：纯格式变更不新增行为测试。

## rust-docs

Clippy补充场景：all是否所有lint、类别默认等级、restriction整组、clippy.toml能否设等级/搜索路径、-p与 -- --no-deps、fix隐含all-targets、driver非生产编译、MSRV仅部分lint、不稳定属性和CI新旧选项。通过条件以2026-10-05已读取的stable入口/usage/configuration为依据，不能把master或新配置强推旧工具链。

输入：项目 MSRV=1.70，edition=2021，tokio 锁定1.28.2且default-features=false/features=[rt]。同事找到 latest docs 的 tokio::net 和最新标准库API就建议照用。查询一个API时应该查哪里、版本怎么匹配、打不开网页怎么回答？同时问Rust语言规则和Cargo features；不要真实查询 tokio 网络，说明方法即可。

通过：docs.rs精确1.28.2，不用latest替代；tokio net feature门控不能从docs.rs全部features推断当前启用；标准库stable文档仍需检查 since/MSRV；edition不等于Rust版本；Reference/Book/Cargo Book来源分工；离线doc/source或明确未核实；输出版本、链接、限制与条件结论，不编造已访问页面。

## rust-crates-first

输入：用户要Rust cron调度，MSRV1.70，没指定依赖或自写；负责人称几十行拆字符串即可、十分钟截止，记得可能有crate但没查过。明确第一个行动、选择及证据。后续查询超时且本地没缓存，负责人催先自写。反例：用户明确为了学习自己实现不要第三方；标准库trim已有；旧Cargo无info/add且默认私有registry；候选latest需新Rust但某历史版可能兼容；候选只有下载数高但功能缺失。

通过：实现新能力前确实安排crates.io查询，不能以简单/赶时间/记得crate为由跳过；仅std/项目已有足够或用户明确自写/禁第三方可跳过。搜索关键词/同义词并核实候选API，选择版本、MSRV/传递依赖、features/target/许可/维护。查询失败不称无实现，不因负责人催促自动自写；说明缺证，重试替代可用渠道/已有资料，仍阻塞时向用户确认是否采用自写例外。显式crates.io而非默认私有registry；不强制升级Cargo，不用不存在的info/add。候选不适配说明具体原因；不把流行度或“我能几行写”当拒绝复用依据。不擅自升级/加依赖/改lock；任务需要依赖可合理集成，无额外泛化审批流。
