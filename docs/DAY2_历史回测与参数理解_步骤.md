# Day 2：历史回测与参数理解（具体步骤）

本文为《VeighNa 入门到实盘 5 天计划书》Day 2 的可执行步骤说明，目标是用历史数据跑通 MyFirstStrategy 回测，看懂回测结果与主要参数，为仿真/实盘打基础。

---

## 目标与产出

- **目标**：用历史数据跑通该策略，看懂回测结果与主要参数（rate、slippage、size、pricetick、capital 等）。
- **产出**：同一策略在指定合约与时间区间上的回测结果与简单结论。

---

## 前置条件

- 已完成 [Day 1](DAY1_环境与第一个CTA策略_步骤.md)：VeighNa Trader 可启动，策略 `MyFirstStrategy` 已出现在【CTA策略】下拉框中。
- 回测依赖**历史 K 线数据**，需先具备其一：
  - 在 Trader 中通过【历史数据管理】下载/导入数据，或
  - 配置 datafeed（如 RQData、TuShare）并在回测前完成数据服务初始化。

---

## 方式 A：Trader 图形界面回测（推荐先做）

### 1. 准备历史数据

- 打开 VeighNa Trader，进入【功能】→【CTA回测】。
- 若尚未有数据，先在回测界面或【历史数据管理】中下载数据：
  - **本地代码**：vt_symbol，如 `IF888.CFFEX`、`rb2505.SHFE`（必须带交易所后缀）。
  - **K 线周期**：1m（1 分钟）、1h、d、w 等。
  - **开始/结束日期**：yyyy/mm/dd。
- 数据来源可为已配置的 datafeed（如 RQData），或从 IB 等已连接接口获取；详见 [CTA回测 - 下载数据](community/app/cta_backtester.md)、[DataManager](community/app/data_manager.md)。

### 2. 执行回测

- 在 CTA回测界面配置：
  - **交易策略**：下拉选择 **MyFirstStrategy**。
  - **本地代码**：与数据一致，如 `IF888.CFFEX`（勿漏交易所后缀）。
  - **数据范围**：K 线周期、开始日期、结束日期。
  - **交易成本**：滑点、百分比手续费（填小数，如 0.3/10000 即填 0.00003 或按界面说明）。
  - **合约属性**：合约乘数（如 IF 为 300）、价格跳动（如 0.2）、回测资金（如 1_000_000）。
- 点击【开始回测】，在策略参数对话框中确认或修改参数后点击【确定】。
- 回测完成后，右侧会显示统计指标与图表。

### 3. 查看结果

- 关注：总收益率、年化收益、最大回撤、总手续费、总滑点、总成交笔数、Sharpe 等。
- 若无数据或数据不足，日志会提示「历史数据不足，回测终止」，需先完成数据准备。

---

## 方式 B：脚本或 Notebook 回测

### 使用 BacktestingEngine

使用 [vnpy_ctastrategy.backtesting.BacktestingEngine](https://github.com/vnpy/vnpy_ctastrategy)，与 [examples/cta_backtesting/backtesting_demo.ipynb](../examples/cta_backtesting/backtesting_demo.ipynb) 用法一致，将策略类改为 `MyFirstStrategy` 即可。

**关键参数说明（set_parameters）**：

| 参数 | 含义 | 对结果的影响 |
|------|------|--------------|
| vt_symbol | 合约 vt_symbol，如 `IF888.CFFEX` | 决定回测标的与从数据库/datafeed 加载的 K 线。 |
| interval | K 线周期，如 `1m`、`1h`、`d` | 影响回放粒度和策略 on_bar 调用频率。 |
| start / end | 回测起止日期（datetime） | 决定回测区间。 |
| rate | 手续费率（按成交金额比例） | 越大，净收益越低，总手续费越高。 |
| slippage | 滑点（价格单位） | 越大，模拟成本越高，净收益越低。 |
| size | 合约乘数 | 影响每笔盈亏与资金曲线尺度。 |
| pricetick | 最小价格变动 | 影响下单价格取整与撮合逻辑。 |
| capital | 初始资金 | 影响资金曲线起点与收益率分母。 |

**示例代码（需先有历史数据或已配置 datafeed）**：

```python
from datetime import datetime

from vnpy_ctastrategy.backtesting import BacktestingEngine

# 策略放在运行目录 strategies 下时可直接导入
from strategies.my_first_strategy import MyFirstStrategy

engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="IF888.CFFEX",
    interval="1m",
    start=datetime(2019, 1, 1),
    end=datetime(2019, 4, 30),
    rate=0.3 / 10000,
    slippage=0.2,
    size=300,
    pricetick=0.2,
    capital=1_000_000,
)
engine.add_strategy(MyFirstStrategy, {})
engine.run_backtesting()
engine.calculate_result()
engine.calculate_statistics()
engine.show_chart()
```

若脚本不在 Trader 运行目录下，需将运行目录或 `examples/veighna_trader` 加入 `sys.path`，以便 `from strategies.my_first_strategy import MyFirstStrategy` 能找到策略；或使用本仓库提供的 [run_my_first_backtest.py](../examples/cta_backtesting/run_my_first_backtest.py)（见下一节）。

---

## 一键脚本示例（run_my_first_backtest.py）

仓库在 [examples/cta_backtesting/run_my_first_backtest.py](../examples/cta_backtesting/run_my_first_backtest.py) 提供了针对 MyFirstStrategy 的回测脚本，便于在已有历史数据或 datafeed 时一键运行。

- **依赖**：需先有对应 vt_symbol 与区间内的历史 K 线（通过 Trader【历史数据管理】下载或配置 datafeed 后由引擎拉取）。
- **运行方式**：在 `examples/cta_backtesting` 目录下执行（使用项目 .venv 时）：
  ```bat
  ..\..\.venv\Scripts\python.exe run_my_first_backtest.py
  ```
  或先 `cd` 到 Trader 运行目录（含 `strategies` 的目录）再以脚本方式运行，确保能导入 `strategies.my_first_strategy`。
- **说明**：脚本内通过 `sys.path` 将 `examples/veighna_trader` 加入路径，从而导入 `MyFirstStrategy`；回测参数可在脚本内修改。

---

## 数据来源说明

- **历史数据管理**：Trader 中【功能】→【历史数据管理】，可导入 CSV 或通过已配置 datafeed 下载到本地数据库；回测时从数据库读取。参见 [DataManager](community/app/data_manager.md)。
- **datafeed**：在【系统】→【全局配置】中配置 datafeed.name 及账号信息（如 vnpy_rqdata、vnpy_tushare），并安装对应包；打开 CTA回测或运行回测脚本时会尝试从 datafeed 拉取历史数据。若未配置，会提示「没有正确配置数据服务」，需先配置或使用本地已下载数据。

---

## 验收标准

- 回测能完整跑完，无「历史数据不足」等终止报错。
- 能查看统计结果：如总收益率、最大回撤、总手续费、总滑点、交易日数、Sharpe 等。
- 能说出 **rate**（手续费率）、**slippage**（滑点）、**size**（合约乘数）、**pricetick**（最小变动）对回测结果的大致影响（例如：rate/slippage 越大，净收益越低；size 影响单笔盈亏规模）。

---

## 常见问题

- **历史数据不足，回测终止**：该 vt_symbol 在选定区间内没有足够 K 线，需先在【历史数据管理】下载或配置 datafeed 后重试。
- **找不到策略类**：确保策略文件在 Trader **运行目录**下的 `strategies` 文件夹中（与 Day 1 一致）；脚本回测时运行目录或 `veighna_trader` 需在 `sys.path` 中。
- **本地代码缺失交易所后缀**：vt_symbol 必须为「合约.交易所」格式，如 `IF888.CFFEX`。

---

## 下一步

完成 Day 2 后，可进入 [Day 3：SimNow 仿真与策略实盘形态验证](5_DAY_LIVE_TRADING_PLAN.md#day-3simnow-仿真与策略实盘形态验证)。

---

## 参考文档

- [CTA回测](community/app/cta_backtester.md)
- [历史数据管理](community/app/data_manager.md)
- [5 天计划书 - Day 2](5_DAY_LIVE_TRADING_PLAN.md#day-2历史回测与参数理解)
- [backtesting_demo.ipynb](../examples/cta_backtesting/backtesting_demo.ipynb)
