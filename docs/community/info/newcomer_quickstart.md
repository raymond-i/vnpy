# 新同学编程入门与实操

本文按顺序给出可执行步骤和最小示例代码，新同学照做即可完成「环境 → 第一个策略 → 回测 → 实盘加载」全流程。每步都标明「做了什么、如何验证」。

## 前置与环境

- **需要**：Python 3.10 或 3.11、能运行终端与代码的 IDE（如 PyCharm 或 VS Code）。
- **安装 VeighNa**：请按 [Windows 安装](../install/windows_install.md) 完成 VeighNa Studio 或 pip 方式安装。
- **验收**：在命令行执行 `python` 进入解释器后，能成功执行 `import vnpy` 且无报错；若使用 CTA 回测，还需安装 `vnpy_ctastrategy`、`vnpy_ctabacktester` 等（VeighNa Studio 已包含常用模块）。

## 第一步：写一个最小可运行的 CTA 策略

**目标**：一个文件、一个类，继承 `CtaTemplate`，具备最小必需结构，能通过回测跑通（本示例不实际发单，只做结构演示）。

**做法**：在本地任意目录新建 Python 文件（如 `my_first_strategy.py`），复制下面完整代码并保存。注释中标明了「必须保留」的部分，其余可按需扩展。

```python
from vnpy_ctastrategy import CtaTemplate
from vnpy.trader.utility import BarGenerator, ArrayManager

class MyFirstStrategy(CtaTemplate):
    """最小可运行 CTA 策略示例，仅演示结构，不发出交易指令。"""

    author = "新同学"

    # 策略参数（可在界面中修改）
    fast_window = 5
    slow_window = 20

    # 策略变量（运行中会变化，需放入 variables 才能在界面显示）
    fast_ma = 0.0
    slow_ma = 0.0

    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma", "slow_ma"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)  # 必须保留
        self.bg = BarGenerator(self.on_bar)   # Tick 合成 1 分钟 K 线
        self.am = ArrayManager()               # K 线序列，用于算指标

    def on_init(self):
        """策略初始化时调用，加载历史数据。"""
        self.write_log("策略初始化")
        self.load_bar(10)  # 加载最近 10 天数据，供 ArrayManager 计算指标

    def on_start(self):
        """策略启动时调用。"""
        self.write_log("策略启动")

    def on_bar(self, bar):
        """收到一根 K 线时调用，这里是策略逻辑的入口。"""
        self.am.update_bar(bar)
        if not self.am.inited:
            return
        # 以下为示例：计算两根均线（实际发单需调用 self.buy() / self.sell() 等）
        self.fast_ma = self.am.sma(self.fast_window)
        self.slow_ma = self.am.sma(self.slow_window)
        self.put_event()  # 刷新界面显示
```

**说明**：策略文件可先放在任意目录；下一步若用 CtaBacktester 图形界面回测，需把该文件复制到 Trader 运行目录下的 `strategies` 目录才能被识别。

## 第二步：用历史数据回测该策略

**目标**：用一段历史数据跑通策略，并看到统计结果。

### 方式 A：使用 CtaBacktester 图形界面（推荐先熟悉界面）

1. 启动 VeighNa Trader（通过 VeighNa Station 或脚本），并确保已加载 CtaBacktester 模块。
2. 将你在第一步写的策略文件（如 `my_first_strategy.py`）放到 **Trader 运行目录**下的 `strategies` 目录中（运行目录路径见 Trader 主窗口标题栏）。
3. 打开【功能】→【CTA回测】，按界面提示：先下载或选择合约与 K 线周期、起止日期，再选择策略类「MyFirstStrategy」，设置参数后点击运行回测。
4. 详细操作步骤见 [CTA回测](../app/cta_backtester.md)。

**验收**：回测能跑完，并输出统计结果（如收益、回撤、交易日数等）。

### 方式 B：用 Jupyter 或 Python 脚本跑回测

1. 打开或新建 Jupyter Notebook（如 `jupyter lab`），或将下列代码保存为 `.py` 脚本。
2. 将第一步的策略类引入（若策略在 `my_first_strategy.py`，需保证该文件在 Python 路径下），然后创建回测引擎、设置合约与时间区间、添加策略并运行。

示例（需根据你的策略文件路径修改 import）：

```python
from datetime import datetime
from vnpy_ctastrategy.backtesting import BacktestingEngine
# 若策略保存在 my_first_strategy.py，且当前目录即该文件所在目录：
from my_first_strategy import MyFirstStrategy

engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="IF888.CFFEX",
    interval="1m",
    start=datetime(2019, 1, 1),
    end=datetime(2019, 4, 30),
    rate=0.3/10000,
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

3. 更多脚本示例见仓库 [examples/cta_backtesting/backtesting_demo.ipynb](https://github.com/vnpy/vnpy/blob/master/examples/cta_backtesting/backtesting_demo.ipynb)。

**验收**：脚本或 Notebook 能跑完并输出统计或图表。

## 第三步：在 VeighNa Trader 中加载策略（实盘/模拟）

**目标**：在 Trader 的 CTA 策略模块中添加并启动你的策略实例（实盘或模拟前需先连接交易接口）。

**步骤概要**：

1. 启动 VeighNa Trader，连接交易接口（如 CTP 模拟或实盘），直到日志中出现「合约信息查询成功」。
2. 确认策略文件已放在运行目录的 `strategies` 下。
3. 打开【功能】→【CTA策略】，在左上角下拉框中选择你的策略类（如 MyFirstStrategy），点击【添加策略】。
4. 在弹窗中填写实例名称、合约品种（vt_symbol，如 `IF888.CFFEX`）、参数等，点击【添加】。
5. 在左侧策略列表中选中该实例，先点击【初始化】，等待初始化完成后再点击【启动】。

详细说明与截图见 [CTA策略](../app/cta_strategy.md) 的「启动模块」与「添加策略」部分。

## 版本控制与后续学习

- **用 Git 管理策略代码**：若希望完整记录每次修改并便于部署，可参考 [基于 Fork 的 Git 版本控制与策略开发](git_strategy_development.md)。
- **深入 CtaTemplate、BarGenerator、ArrayManager**：完整回调说明、参数与变量、发单接口等，见 [CTA策略 - CTA策略模板](../app/cta_strategy.md#cta策略模板ctatemplate)。
- **更多示例**：仓库 `examples` 目录下有 cta_backtesting、veighna_trader 等示例，可对照学习。
