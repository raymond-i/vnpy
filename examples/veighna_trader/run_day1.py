"""
Day 1 最小启动脚本：仅加载 CTA 策略与回测模块，无需连接交易接口。
用于验证环境与策略加载；完成 Day 1 后可用 run.py 加载 CTP 等。
"""
from vnpy.event import EventEngine

from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_ctastrategy import CtaStrategyApp
from vnpy_ctabacktester import CtaBacktesterApp


def main():
    """Start VeighNa Trader for Day 1 (no gateway)."""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    # Day 1: 仅 CTA 策略与回测，无需 Gateway
    main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(CtaBacktesterApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
