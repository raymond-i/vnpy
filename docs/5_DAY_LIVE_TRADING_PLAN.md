# VeighNa 入门到实盘 5 天计划书

## 目标与前提

- **目标**：5 天内完成从零到「可实盘运行 CTA 策略」的全流程（环境 → 策略 → 回测 → 仿真 → 实盘）。
- **前提**：具备基本 Python 能力；实盘需已拥有期货账户（或至少已在开户流程中），并能在第 4–5 天拿到实盘/仿真环境与配置。
- **风险提示**：实盘涉及真实资金，计划中第 5 天建议先小资金或短时验证，再逐步放大。

---

## 整体节奏示意

```mermaid
flowchart LR
    D1[Day1 环境与策略]
    D2[Day2 回测]
    D3[Day3 仿真]
    D4[Day4 风控与实盘准备]
    D5[Day5 实盘]
    D1 --> D2 --> D3 --> D4 --> D5
```

---

## Day 1：环境搭建与第一个 CTA 策略

**目标**：环境可运行 VeighNa Trader，能写一个最小可运行的 CTA 策略并在本地被正确加载。

| 项目               | 内容                                                                                                                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **环境**           | 安装 [VeighNa Studio](https://download.vnpy.com/veighna_studio-4.3.0.exe)（推荐）或按 [Windows 安装](community/install/windows_install.md) 用 pip 安装；确保含 `vnpy_ctastrategy`、`vnpy_ctabacktester`、`vnpy_ctp`（或你计划用的网关）。    |
| **验收**           | 命令行 `import vnpy` 无报错；通过 VeighNa Station 能启动 VeighNa Trader。                                                                                                                                                        |
| **第一个策略**        | 按 [新同学编程入门与实操](community/info/newcomer_quickstart.md) 第一步：新建 `my_first_strategy.py`，写一个继承 `CtaTemplate` 的最小策略（含 `BarGenerator`、`ArrayManager`、`on_init`/`on_start`/`on_bar`、`parameters`/`variables`），不要求真实发单。 |
| **Trader 与策略目录** | 用 [examples/veighna_trader/run.py](../examples/veighna_trader/run.py) 或 Station 启动 Trader，确认运行目录；把策略文件放到运行目录下的 `strategies` 文件夹，以便后续回测与实盘加载。                                                                           |

**产出**：可运行的 VeighNa 环境 + 一个最小 CTA 策略文件（在 `strategies` 下）。

---

## Day 2：历史回测与参数理解

**目标**：用历史数据跑通该策略，看懂回测结果与主要参数，为仿真/实盘打基础。

| 项目               | 内容                                                                                                                                                                                                                          |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **回测方式 A（推荐先做）** | 在 Trader 中打开【功能】→【CTA回测】，选择合约（如 `IF888.CFFEX`）、K 线周期与起止时间，选择你的策略类并运行；参考 [CTA回测](community/app/cta_backtester.md)。                                                                                                      |
| **回测方式 B**       | 使用 [examples/cta_backtesting/backtesting_demo.ipynb](../examples/cta_backtesting/backtesting_demo.ipynb) 或脚本方式调用 `BacktestingEngine`，设置 `vt_symbol`、`interval`、`start`/`end`、`rate`/`slippage`/`size`/`pricetick`/`capital` 等。 |
| **数据来源**         | 若 Trader 内无数据，先用【历史数据管理】或数据服务（如有）下载对应合约 K 线；见 [DataManager](community/app/data_manager.md)。                                                                                                                            |
| **验收**           | 回测跑完并得到统计结果（收益、回撤、交易日等）；能说出 `rate`、`slippage`、`size`、`pricetick` 对结果的大致影响。                                                                                                                                                  |

**产出**：同一策略在指定合约与区间上的回测结果与简单结论。

---

## Day 3：SimNow 仿真与策略实盘形态验证

**目标**：用 SimNow CTP 仿真连接 Trader，在「实盘形态」下跑同一策略（初始化 → 启动 → 看日志与持仓），不追求盈利，只验证流程。

| 项目                  | 内容                                                                                                                                                                                           |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SimNow 账号**       | 在 [SimNow](http://www.simnow.com.cn/) 注册并获取仿真账号；[SimNow 产品页](http://www.simnow.com.cn/product.action) 获取经纪商代码（9999）及交易/行情服务器地址；首次登录需修改密码。详见 [gateway - CTP](community/info/gateway.md)。 |
| **连接 CTP**          | 在 Trader 中【系统】→【连接 CTP】，填入用户名、密码、经纪商 9999、交易/行情服务器等；确认日志出现「合约信息查询成功」。参考 [VeighNa Trader - SimNow](community/info/veighna_trader.md)。                                                    |
| **加载策略**            | 【功能】→【CTA策略】→ 选择你的策略类 →【添加策略】→ 填实例名称、`vt_symbol`（与回测一致）、参数 →【添加】→ 选中实例后先【初始化】再【启动】。见 [newcomer_quickstart 第三步](community/info/newcomer_quickstart.md)。                                  |
| **可选：PaperAccount** | 若希望用「本地仿真」先练手，可安装并加载 [PaperAccount](community/app/paper_account.md)，用实盘行情做本地撮合，再切 SimNow。                                                                                               |
| **验收**              | 策略在 SimNow 下能完成初始化与启动，日志无「行情订阅失败」等错误；若有简单开平逻辑，能看到委托/成交/持仓变化。                                                                                                                                 |

**产出**：SimNow 下策略从初始化到运行的完整流程跑通。

---

## Day 4：风控、实盘准备与检查清单

**目标**：了解 Trader 风控与日志，完成实盘前检查清单，并准备好实盘账号与配置（若尚未开户则完成申请与配置准备）。

| 项目          | 内容                                                                                                             |
| ----------- | -------------------------------------------------------------------------------------------------------------- |
| **风险管理**    | 若有 [RiskManager](community/app/risk_manager.md)，在 Trader 中配置流控、单笔/总委托量、撤单次数等限制；理解「实盘前必开风控」的意义。            |
| **日志与监控**   | 熟悉 Trader 日志位置与级别；确认能根据日志排查「连接失败、合约未找到、初始化失败」等常见问题；见 [CTA策略 - 实盘运行](community/app/cta_strategy.md) 中的注意点。 |
| **实盘账号与配置** | 若未开户：联系期货公司开通账户及 CTP 接入（含经纪商代码、交易/行情地址）；若已开户：向客户经理索取实盘 CTP 参数（或仿真环境参数），并区分「实盘」与「仿真」配置，避免误用。                    |
| **检查清单**    | 策略在回测和 SimNow 下均跑过；`vt_symbol`、合约乘数、保证金、手续费在实盘侧已确认；风控已配置；实盘配置单独保存且与 SimNow 区分；计划首日使用小资金或最小手数。                  |

**产出**：风控配置 + 实盘（或仿真）连接参数 + 实盘前检查清单勾选完成。

---

## Day 5：实盘部署与首日监控

**目标**：使用实盘（或期货公司提供的仿真）环境连接 Trader，小资金/最小手数运行策略，并完成首日监控与收尾。

| 项目         | 内容                                                                                                 |
| ---------- | -------------------------------------------------------------------------------------------------- |
| **连接实盘环境** | 在 Trader 中【系统】→【连接 CTP】，填入**实盘**经纪商代码与服务器（勿与 SimNow 混用）；确认登录成功与合约查询成功。                             |
| **策略加载**   | 与 Day 3 相同：【CTA策略】→ 添加策略实例 → 初始化 → 启动；确认合约与参数与回测/仿真一致，且为实盘可交易合约。                                   |
| **首日建议**   | 使用小资金或单合约最小手数；可先观察 1～2 根 K 线再决定是否保持运行；盘中关注日志与持仓、委托列表。                                              |
| **盘后**     | 停止策略、关闭 Trader 前确认无挂单遗留；若有需要，可配合 [DataRecorder](community/app/data_recorder.md) 录制行情供日后回测或复盘。 |

**产出**：实盘（或仿真）环境下策略已运行并完成首日监控；形成「连接 → 初始化 → 启动 → 监控 → 停止」的固定流程。

---

## 文档与示例索引

| 用途                  | 文档/示例                                                                                              |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| 环境与第一步策略、回测、实盘加载    | [community/info/newcomer_quickstart.md](community/info/newcomer_quickstart.md)           |
| CTA 策略模板、回调、发单、实盘注意 | [community/app/cta_strategy.md](community/app/cta_strategy.md)                           |
| CTA 回测操作            | [community/app/cta_backtester.md](community/app/cta_backtester.md)                       |
| CTP/SimNow 账号与配置    | [community/info/gateway.md](community/info/gateway.md)、[README 使用指南](../README.md)          |
| 脚本回测示例              | [examples/cta_backtesting/backtesting_demo.ipynb](../examples/cta_backtesting/backtesting_demo.ipynb) |
| Trader 启动示例         | [examples/veighna_trader/run.py](../examples/veighna_trader/run.py)                                   |

---

## 小结

- **Day 1**：环境 + 最小 CTA 策略 + 放入 `strategies`。  
- **Day 2**：同一策略历史回测 + 理解关键参数与结果。  
- **Day 3**：SimNow 连接 + 策略初始化/启动，验证实盘形态流程。  
- **Day 4**：风控与日志 + 实盘账号与配置 + 实盘前检查清单。  
- **Day 5**：实盘（或期货公司仿真）连接 + 小资金/最小手数运行 + 首日监控与收尾。

按上述顺序执行并严格区分 SimNow 与实盘配置，可在 5 天内完成从入门到实盘的首轮闭环；后续再逐步做参数优化、多策略与风控细化。
