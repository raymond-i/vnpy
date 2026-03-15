"""
Day 2 示例：使用 MyFirstStrategy 进行 CTA 回测。

运行前请确保已有历史 K 线数据：
- 在 VeighNa Trader 中通过【历史数据管理】下载/导入，或
- 在【全局配置】中配置 datafeed（如 vnpy_rqdata、vnpy_tushare）后由回测引擎拉取。

使用方式（在项目根目录或 examples/veighna_trader 下执行时，可直接用 strategies 目录）：
  python examples/cta_backtesting/run_my_first_backtest.py

或进入 examples/cta_backtesting 后（需将 veighna_trader 加入路径）：
  ..\..\.venv\Scripts\python.exe run_my_first_backtest.py
"""
from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime

# 将 veighna_trader 加入路径，以便导入 strategies.my_first_strategy
_script_dir = Path(__file__).resolve().parent
_veighna_trader = _script_dir.parent / "veighna_trader"
if _veighna_trader.exists() and str(_veighna_trader) not in sys.path:
    sys.path.insert(0, str(_veighna_trader))

from vnpy_ctastrategy.backtesting import BacktestingEngine

from strategies.my_first_strategy import MyFirstStrategy


def main() -> None:
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


if __name__ == "__main__":
    main()
