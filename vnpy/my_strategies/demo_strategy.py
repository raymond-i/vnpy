from vnpy_ctastrategy import CtaTemplate
from vnpy.trader.utility import BarGenerator, ArrayManager

class MyDemoStrategy(CtaTemplate):
    author = "Raymond"

    # ... 策略参数和变量定义 ...

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    def on_tick(self, tick):
        self.bg.update_tick(tick)

    def on_bar(self, bar):
        # ... 核心交易逻辑（计算指标、判断多空、发单操作） ...
        self.put_event()