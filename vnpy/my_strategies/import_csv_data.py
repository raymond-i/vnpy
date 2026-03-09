import pandas as pd
from datetime import datetime
from pytz import timezone

# 导入 vn.py 核心组件
from vnpy.trader.object import BarData
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import get_database


def clean_and_import_data(csv_file_path: str, symbol: str, exchange: Exchange, interval: Interval):
    print(f"开始读取 CSV 文件: {csv_file_path}")

    # 1. 使用 pandas 读取 CSV
    # 假设你的 CSV 列名为: datetime, open, high, low, close, volume, open_interest
    df = pd.read_csv(csv_file_path)

    # 2. 数据清洗 (Data Cleaning)
    # 丢弃包含空值的异常行
    df.dropna(inplace=True)

    # 将字符串格式的时间转换为 pandas 的 datetime 对象
    df['datetime'] = pd.to_datetime(df['datetime'])

    # 3. 构建 BarData 对象列表
    china_tz = timezone("Asia/Shanghai")
    bars = []

    print("正在清洗并转换数据...")
    for row in df.itertuples():
        # 给 datetime 添加本地时区信息 (极易出错的坑点)
        dt = row.datetime.replace(tzinfo=china_tz)

        # 组装 vn.py 标准的 BarData 对象
        bar = BarData(
            symbol=symbol,
            exchange=exchange,
            datetime=dt,
            interval=interval,
            volume=row.volume,
            open_price=row.open,
            high_price=row.high,
            low_price=row.low,
            close_price=row.close,
            open_interest=row.open_interest,
            gateway_name="DB"  # 标识数据来源为数据库
        )
        bars.append(bar)

    # 4. 批量写入 SQLite 数据库
    print(f"数据转换完成，共计 {len(bars)} 条 K 线，准备写入数据库...")
    database_manager = get_database()

    # save_bar_data 内部封装了批量插入逻辑，性能很好
    database_manager.save_bar_data(bars)
    print("数据成功写入 SQLite 数据库！")


if __name__ == "__main__":
    # 模拟执行：假设你有一份下载好的 rb888_1min.csv 文件
    # 文件路径请替换为你电脑上的真实路径
    csv_path = "rb888_1min.csv"

    try:
        clean_and_import_data(
            csv_file_path=csv_path,
            symbol="rb888",
            exchange=Exchange.SHFE,  # 上期所
            interval=Interval.MINUTE  # 1分钟线
        )
    except FileNotFoundError:
        print(f"错误: 找不到文件 {csv_path}。请先准备好 CSV 数据。")