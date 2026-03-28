"""
Footprint chart demo: synthetic OrderFlowBarData + OrderFlowItem, cumulative delta,
volume profile to the right of the candle pane (Y-linked), and a small settings dialog.

Run locally (requires desktop / PySide6 / pyqtgraph):

    python examples/orderflow_chart/run.py

Drag the chart with the mouse, use the mouse wheel to zoom (same as main chart).
"""

from __future__ import annotations

from datetime import datetime, timedelta

from vnpy.chart import (
    CandleItem,
    ChartWidget,
    CumulativeDeltaItem,
    OrderFlowItem,
    OrderFlowViewSettings,
    VolumeProfileItem,
)
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import OrderBookPriceDetail, OrderFlowBarData
from vnpy.trader.orderflow_aggregate import OrderFlowWindowAggregator
from vnpy.trader.ui import QtWidgets, create_qapp


def _cell(buy: int, sell: int, large: int = 0) -> OrderBookPriceDetail:
    return OrderBookPriceDetail(
        buy_vol=buy, sell_vol=sell, total_vol=buy + sell, large_tick_count=large
    )


def build_demo_bars() -> list[OrderFlowBarData]:
    base = datetime(2025, 3, 22, 9, 0, 0)
    bars: list[OrderFlowBarData] = []
    # Bar 0: two levels + imbalance-style ratio on upper leg
    b0 = OrderFlowBarData(
        symbol="rb2505",
        exchange=Exchange.SHFE,
        datetime=base,
        gateway_name="DEMO",
        interval=Interval.MINUTE,
        open_price=3500.0,
        high_price=3502.0,
        low_price=3499.0,
        close_price=3501.0,
        volume=120.0,
        order_book_details={
            3499.0: _cell(0, 40),
            3500.0: _cell(30, 20),
            3501.0: _cell(50, 0, large=2),
        },
    )
    b0.finalize_orderflow_metrics(imbalance_threshold_ratio=3.0)
    bars.append(b0)

    b1 = OrderFlowBarData(
        symbol="rb2505",
        exchange=Exchange.SHFE,
        datetime=base + timedelta(minutes=1),
        gateway_name="DEMO",
        interval=Interval.MINUTE,
        open_price=3501.0,
        high_price=3505.0,
        low_price=3500.0,
        close_price=3504.0,
        volume=200.0,
        order_book_details={
            3500.0: _cell(5, 35),
            3502.0: _cell(20, 10),
            3504.0: _cell(80, 15),
        },
    )
    b1.finalize_orderflow_metrics(imbalance_threshold_ratio=3.0)
    bars.append(b1)

    b2 = OrderFlowBarData(
        symbol="rb2505",
        exchange=Exchange.SHFE,
        datetime=base + timedelta(minutes=2),
        gateway_name="DEMO",
        interval=Interval.MINUTE,
        open_price=3504.0,
        high_price=3504.0,
        low_price=3498.0,
        close_price=3499.0,
        volume=90.0,
        order_book_details={
            3498.0: _cell(0, 25),
            3499.0: _cell(40, 10),
            3502.0: _cell(5, 10),
        },
    )
    b2.finalize_orderflow_metrics(imbalance_threshold_ratio=3.0)
    bars.append(b2)

    return bars


def build_demo_3m_bars() -> list[OrderFlowBarData]:
    """Merge three 1m demo bars into one 3m window (BarGenerator-aligned rule)."""
    out: list[OrderFlowBarData] = []
    agg = OrderFlowWindowAggregator(3, out.append, imbalance_threshold_ratio=3.0)
    for b in build_demo_bars():
        agg.update_bar(b)
    return out


def main() -> None:
    app = create_qapp()
    view_settings = OrderFlowViewSettings(price_step=1.0)

    chart = ChartWidget()
    chart.add_plot("candle", hide_x_axis=True)
    chart.add_plot(
        "vp",
        same_row_as="candle",
        link_x_axis=False,
        hide_x_axis=True,
        minimum_width=110,
        maximum_width=240,
    )
    chart.add_plot("cumdelta", maximum_height=140, colspan=2)

    chart.add_item(CandleItem, "candle", "candle")
    chart.add_item(
        OrderFlowItem,
        "footprint",
        "candle",
        settings=view_settings,
        default_price_step=1.0,
    )
    chart.add_item(CumulativeDeltaItem, "cumdelta", "cumdelta")
    chart.add_item(VolumeProfileItem, "vp", "vp", price_step=1.0)
    chart.add_cursor()

    c_plot = chart.get_plot("candle")
    vp_plot = chart.get_plot("vp")
    if c_plot is not None and vp_plot is not None:
        vp_plot.setYLink(c_plot)
        # Price scale on main pane only; VP column stays narrow.
        vp_plot.hideAxis("right")

    bars_1m = build_demo_bars()
    chart.update_history(bars_1m)

    foot_item: OrderFlowItem = chart._items["footprint"]  # noqa: SLF001
    vp_item: VolumeProfileItem = chart._items["vp"]  # noqa: SLF001

    win = QtWidgets.QMainWindow()
    win.setWindowTitle("Order flow demo (VeighNa chart)")
    central = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(central)

    bar_btns = QtWidgets.QHBoxLayout()
    btn_1m = QtWidgets.QPushButton("数据：1 分钟")
    btn_3m = QtWidgets.QPushButton("数据：3 分钟合成")
    bar_btns.addWidget(btn_1m)
    bar_btns.addWidget(btn_3m)
    bar_btns.addStretch(1)
    layout.addLayout(bar_btns)

    btn_settings = QtWidgets.QPushButton("足迹显示参数…")
    layout.addWidget(btn_settings)
    layout.addWidget(chart, stretch=1)
    win.setCentralWidget(central)
    win.resize(960, 720)

    def reload_1m() -> None:
        chart.clear_all()
        chart.update_history(build_demo_bars())

    def reload_3m() -> None:
        chart.clear_all()
        chart.update_history(build_demo_3m_bars())

    btn_1m.clicked.connect(reload_1m)
    btn_3m.clicked.connect(reload_3m)

    def open_settings() -> None:
        d = QtWidgets.QDialog(win)
        d.setWindowTitle("足迹显示参数")
        form = QtWidgets.QFormLayout(d)
        sp_font = QtWidgets.QDoubleSpinBox()
        sp_font.setRange(0.35, 3.0)
        sp_font.setSingleStep(0.05)
        sp_font.setValue(view_settings.font_scale)
        sp_heat = QtWidgets.QDoubleSpinBox()
        sp_heat.setRange(0.2, 2.5)
        sp_heat.setSingleStep(0.05)
        sp_heat.setValue(view_settings.heat_intensity)
        sp_step = QtWidgets.QDoubleSpinBox()
        sp_step.setRange(0.25, 20.0)
        sp_step.setSingleStep(0.25)
        sp_step.setValue(view_settings.price_step or 1.0)
        chk_large = QtWidgets.QCheckBox("大单角标")
        chk_large.setChecked(view_settings.large_trade_marker)
        form.addRow("字体缩放", sp_font)
        form.addRow("热力强度", sp_heat)
        form.addRow("价格步长 (与 VP 同步)", sp_step)
        form.addRow(chk_large)
        bb = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        form.addRow(bb)
        bb.accepted.connect(d.accept)
        bb.rejected.connect(d.reject)
        if d.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        view_settings.font_scale = sp_font.value()
        view_settings.heat_intensity = sp_heat.value()
        view_settings.price_step = sp_step.value()
        view_settings.large_trade_marker = chk_large.isChecked()
        foot_item.apply_settings(view_settings)
        vp_item.set_price_step(view_settings.price_step)

    btn_settings.clicked.connect(open_settings)

    win.show()
    app.exec()


if __name__ == "__main__":
    main()
