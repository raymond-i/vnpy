from datetime import datetime
from vnpy_ctastrategy.backtesting import BacktestingEngine
# 这里导入你写的策略类，假设文件名为 demo_strategy.py
from my_strategies.demo_strategy import MyDemoStrategy


def run_test_case():
    # 1. Setup: 初始化回测引擎 (搭建测试环境)
    engine = BacktestingEngine()

    # 2. Setup: 配置测试参数 (模拟真实的实盘环境损耗)
    engine.set_parameters(
        vt_symbol="rb888.SHFE",  # 被测品种：螺纹钢主力连续合约
        interval="1m",  # 数据级别：1分钟线
        start=datetime(2025, 1, 1),  # 测试区间起点
        end=datetime(2025, 12, 31),  # 测试区间终点
        rate=0.0001,  # 手续费率 (模拟交易成本)
        slippage=1,  # 滑点 (模拟真实市场中吃单产生的点差损耗)
        size=10,  # 合约乘数 (1手螺纹钢=10吨)
        pricetick=1,  # 价格最小跳动单位
        capital=1_000_000,  # 初始测试资金
    )

    # 3. Setup: 加载被测对象和测试数据
    # 传入策略类，以及你想测试的参数组合
    engine.add_strategy(MyDemoStrategy, {"fast_window": 10, "slow_window": 20})
    engine.load_data()  # 从本地数据库读取指定区间的 rb888 历史数据

    # 4. Run: 执行自动化回测 (逐根 K 线推送给策略执行)
    print("开始运行自动化回测...")
    engine.run_backtesting()

    # 5. Report: 计算绩效并输出结果 (生成测试报告)
    df = engine.calculate_result()  # 计算逐日盯市盈亏
    metrics = engine.calculate_statistics()  # 计算核心绩效指标

    # 打印核心验证指标
    print("-" * 30)
    print(f"总收益率: {metrics['total_return']:,.2f}%")
    print(f"最大回撤: {metrics['max_drawdown']:,.2f}%")
    print(f"夏普比率: {metrics['sharpe_ratio']:,.2f}")

    # 绘制可视化资金曲线
    engine.show_chart()


if __name__ == "__main__":
    run_test_case()