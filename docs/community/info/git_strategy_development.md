# 基于 Fork 的 Git 版本控制与策略开发

本文面向希望使用 Git 做完整版本控制、并可能阅读或修改 vn.py（VeighNa）框架底层代码的开发者。若仅编写个人策略而不改框架，更推荐使用独立策略仓库 + 将 vn.py 作为依赖的方式；若需魔改引擎（如订单路由等），则 Fork 本仓库并按下文流程操作。

## 架构说明：何时 Fork，何时独立仓库

- **仅编写个人交易策略**：建议新建独立 Git 仓库（如 `my_quant_strategies`），只存放策略脚本，将 vn.py 作为本地 Python 依赖安装。这样与框架解耦，上游更新频繁时不会产生合并冲突。
- **需要深入阅读或魔改 vn.py 底层**（如订单路由、引擎逻辑）：Fork 官方仓库并在本地以可编辑模式安装，便于修改源码并做版本管理。

下文为基于 **Fork 模式** 的完整操作指引。

## 1. 在 GitHub 上 Fork 并拉取代码

1. 登录 GitHub，打开官方仓库 [https://github.com/vnpy/vnpy](https://github.com/vnpy/vnpy)。
2. 点击右上角 **Fork**，将项目复制到你的账号下。
3. 在 Windows Terminal 或命令行中克隆到本地（建议使用全英文路径，避免 C++ 等库加载报错）：

```bash
git clone https://github.com/你的GitHub用户名/vnpy.git
cd vnpy
```

## 2. 在 PyCharm 中配置开发环境

为让 PyCharm 正确识别依赖并令本地修改的源码实时生效，需使用**可编辑模式（Editable mode）**安装。安装后修改本地源码会直接生效，无需重新安装。

1. 打开 PyCharm，选择 **Open**，打开刚克隆的 `vnpy` 目录。
2. 若未自动创建虚拟环境，可在解释器设置中新建基于 Python 3.10 或 3.11 的虚拟环境。
3. 打开底部 **Terminal**（已激活虚拟环境），执行：

```bash
# 以可编辑模式安装当前目录的源码
pip install -e .

# 安装国内商品期货常用的 CTP 接口和 CTA 策略引擎
pip install vnpy_ctp vnpy_ctastrategy
```

> 更多 IDE 配置与断点调试，请参见 [PyCharm 开发指南](pycharm.md)。

## 3. 创建专属的策略开发分支

在主分支上直接开发容易污染历史，建议新建特性分支专门用于策略开发。

在 Terminal 中执行：

```bash
git checkout -b feature/my-cta-strategies
```

之后在该分支上编写和测试策略即可。若需向官方仓库提交 PR，请遵循 [贡献代码](contribution.md) 中的分支与 Pull Request 流程。

## 4. 编写与存放策略代码

可将策略放在官方示例目录，但更推荐在**项目根目录下**新建专属目录便于管理。

1. 在项目树中右键根目录 **vnpy** → **New → Directory**，命名为 `my_strategies`。
2. 在 `my_strategies` 内右键 **New → Python File**，命名为 `demo_strategy.py`。
3. 编写策略逻辑。CTA 策略需继承 `vnpy_ctastrategy` 的 `CtaTemplate`，并配合 `BarGenerator`（K 线合成）与 `ArrayManager`（时间序列）使用，示例结构如下：

```python
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
```

> 在 VeighNa Trader 中实盘或模拟运行时，需将策略放到**运行目录**下的 `strategies` 目录中才能被加载，详见 [CTA策略](../app/cta_strategy.md) 文档。

## 5. 提交与版本控制

完成一个阶段的策略编写或回测通过后，可将代码提交并推送到你自己的 GitHub Fork 仓库。

1. 查看变更状态：

```bash
git status
```

2. 将策略目录加入暂存区并提交：

```bash
git add my_strategies/
git commit -m "feat: 初步完成双均线策略逻辑，并添加 BarGenerator"
```

3. 推送到 Fork 的远程分支：

```bash
git push origin feature/my-cta-strategies
```

若需向官方 vn.py 仓库贡献代码，请按 [贡献代码](contribution.md) 中的分支与 PR 流程操作。

## 延伸阅读

- **历史回测**：编写回测脚本在 PyCharm 中运行，可参考 [CTA回测](../app/cta_backtester.md) 及仓库中的 [回测示例](https://github.com/vnpy/vnpy/blob/master/examples/cta_backtesting/backtesting_demo.ipynb)。
- **策略基础组件**：了解 **BarGenerator**（K 线合成器）与 **ArrayManager**（时间序列数组）的用法，可查阅 vnpy 源码中 `vnpy.trader.utility` 模块及 CTA 策略相关文档。
