"""
Day 1 最小可运行 CTA 策略示例。
用于 5 天入门到实盘计划书 - 仅演示结构，不发出交易指令。
"""
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
