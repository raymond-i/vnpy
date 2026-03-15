# Day 1：环境搭建与第一个 CTA 策略（具体步骤）

本文为《VeighNa 入门到实盘 5 天计划书》Day 1 的可执行步骤说明，按顺序完成即可达成：**环境可运行 VeighNa Trader，并有一个最小可运行的 CTA 策略且能被正确加载**。

---

## 目标与产出

- **目标**：环境可运行 VeighNa Trader，能写一个最小可运行的 CTA 策略并在本地被正确加载。
- **产出**：可运行的 VeighNa 环境 + 一个最小 CTA 策略文件（位于 Trader 运行目录下的 `strategies` 中）。

---

## 步骤一：安装 VeighNa 环境

任选其一即可。

### 方式 A：VeighNa Studio（推荐，尤其适合新手）

1. 在 [VeighNa 官网](https://www.vnpy.com/) 或 [VeighNa Studio 直接下载](https://download.vnpy.com/veighna_studio-4.3.0.exe) 下载安装包。
2. 双击安装包（建议右键选择「使用管理员身份运行」），使用默认设置点击「快速安装」。
3. 推荐安装路径：`C:\veighna_studio`（与文档一致）。
4. 安装完成后，桌面会出现 **VeighNa Station** 图标。

### 方式 B：手动安装（已有 Python 3.10 64 位）

1. 准备 Python 3.10 64 位环境（[Python 官网](https://www.python.org/downloads/windows/) 下载 Windows installer 64-bit），安装时勾选「Add Python 3.10 to PATH」。
2. 从 [VeighNa Releases](https://github.com/vnpy/vnpy/releases) 下载源码（Windows 建议 zip），解压到本地。
3. 打开 CMD 或 PowerShell，进入解压后目录（即与 `install.bat` 同级）：
   ```bat
   cd D:\path\to\vnpy
   install.bat
   ```
4. 等待脚本完成：安装 ta-lib、安装 VeighNa 及依赖。若报错，请保存完整报错信息以便排查。

---

## 步骤二：验收环境

### 若使用本仓库 `.venv`

在项目根目录已存在 `.venv` 且已安装 VeighNa 时，可直接用该虚拟环境。Day 1 需额外安装 CTA 与默认数据库：`pip install vnpy_ctastrategy vnpy_ctabacktester vnpy_sqlite`（在 `.venv` 下执行）。

```bat
d:\word\vnpy\.venv\Scripts\python.exe -c "import vnpy; print(vnpy.__version__)"
```

或进入 `examples\veighna_trader` 后双击运行 `run_day1_with_venv.bat` 启动 Trader（见步骤三）。

### 通用验收

在**同一环境**下（VeighNa Studio 用户从开始菜单或桌面打开「VeighNa Studio 命令行」；手动安装用户使用已安装 Python 的 CMD/PowerShell）执行：

```bash
python
```

进入 Python 后输入：

```python
import vnpy
print(vnpy.__version__)
```

- **验收标准**：无报错，并打印出版本号（如 `4.3.0`）。
- 若使用 CTA 回测与实盘，需确保已安装：`vnpy_ctastrategy`、`vnpy_ctabacktester`、`vnpy_sqlite`（CTA 引擎默认使用 SQLite 存储）、`vnpy_ctp`（连接 CTP 时再装；VeighNa Studio 已包含上述模块；手动安装时 `install.bat` 仅装核心依赖，其余需按需安装）。

---

## 步骤三：启动 VeighNa Trader

### 使用 VeighNa Station（推荐）

1. 双击桌面 **VeighNa Station** 图标。
2. 使用 VeighNa 社区论坛账号登录（若无请先 [注册](https://www.vnpy.com/forum/)）。
3. 点击底部 **VeighNa Trader** 按钮，等待主窗口打开。

### 使用本仓库脚本启动

1. 打开 CMD 或 PowerShell，进入本仓库的示例目录：
   ```bat
   cd d:\word\vnpy\examples\veighna_trader
   ```
2. **Day 1 最小启动**（无需安装 CTP 等交易接口，仅验证策略加载）：
   - 使用本仓库 `.venv` 时，在 `examples\veighna_trader` 目录下执行：
     ```bat
     ..\..\.venv\Scripts\python.exe run_day1.py
     ```
     或直接双击该目录下的 `run_day1_with_venv.bat`。
   - 或在该目录下先激活虚拟环境再执行：
     ```bat
     python run_day1.py
     ```
   若已安装完整依赖并需连接 CTP，再使用：
   ```bat
   python run.py
   ```
3. 本仓库已在 `examples/veighna_trader` 下创建 `.vntrader` 目录，因此从该目录执行上述命令时，**运行目录**即为 `examples\veighna_trader`，策略目录为 `strategies`（其中已包含 `my_first_strategy.py`）。运行目录会显示在 Trader 主窗口标题栏中，例如：`VeighNa Trader 社区版 - 4.3.0   [D:\word\vnpy\examples\veighna_trader]`。

**验收标准**：Trader 主窗口正常打开，无崩溃；标题栏能看到版本号与运行目录路径。

---

## 步骤四：准备第一个 CTA 策略文件

本仓库已提供最小可运行策略，无需手敲代码。

### 策略文件位置（仓库内）

- 路径：[examples/veighna_trader/strategies/my_first_strategy.py](../examples/veighna_trader/strategies/my_first_strategy.py)
- 策略类名：`MyFirstStrategy`
- 功能：继承 `CtaTemplate`，含 `BarGenerator`、`ArrayManager`，实现 `on_init`、`on_start`、`on_bar`，计算双均线并在界面刷新变量；**不发出实际交易指令**。

### 让 Trader 识别到该策略

Trader 只会加载**运行目录**下 `strategies` 文件夹中的策略文件。

- **若你从本仓库 `examples/veighna_trader` 运行 `run.py`**  
  - 若该目录下已有 `.vntrader`，则运行目录即为 `examples/veighna_trader`，策略已在 `strategies/my_first_strategy.py`，无需再复制。
  - 若该目录下没有 `.vntrader`，运行目录一般是用户主目录，请将 `examples/veighna_trader/strategies/my_first_strategy.py` 复制到运行目录下的 `strategies` 文件夹中；若没有 `strategies` 文件夹，请先新建再复制。

- **若你通过 VeighNa Station 启动 Trader**  
  - 运行目录多为用户主目录（见标题栏 `[路径]`）。请在运行目录下新建 `strategies` 文件夹（若不存在），再将仓库中的 `my_first_strategy.py` 复制进去。

示例（运行目录为 `C:\Users\你的用户名` 时）：

```text
C:\Users\你的用户名\
  └── strategies\
        └── my_first_strategy.py
```

---

## 步骤五：在 Trader 中验证策略已加载

1. 在 Trader 中打开【功能】→【CTA策略】。
2. 在左上角策略下拉框中查找 **MyFirstStrategy**，点击【添加策略】。
3. 在弹窗中填写：
   - **实例名称**：任意不重名名称（如 `my_first_1`）。
   - **合约品种**：必须填写 **vt_symbol**，即「合约代码 + 英文点 + 交易所后缀」，不能只填合约代码，否则会报「创建策略失败，本地代码缺失交易所后缀」。示例：
     - 股指期货连续：`IF888.CFFEX`（中金所）
     - 螺纹钢：`rb2505.SHFE`（上期所）
     - 豆粕：`m2505.DCE`（大商所）
     - 甲醇：`MA505.CZCE`（郑商所）
   - **参数**：可保持默认。
4. 点击【添加】。
5. **验收标准**：左侧出现该策略实例，且无报错；下拉框中能看到 `MyFirstStrategy`，说明 Day 1 的策略已可被加载（Day 2 再在回测中运行，Day 3 再在仿真中初始化与启动）。

---

## 关于「没有配置要使用的数据服务」提示

启动后终端可能出现：

```text
没有配置要使用的数据服务，请修改全局配置中的datafeed相关内容
```

- **含义**：**datafeed** 指用于获取历史行情的数据服务（如 RQData、TuShare、Wind 等）。当前未配置 `datafeed.name`，系统使用了空实现，无法拉取历史 K 线/Tick。
- **Day 1 是否需要处理**：**不需要**。Day 1 只要求环境跑通、策略能被识别；不做回测、不初始化策略，不会用到历史数据。
- **何时需要配置**：
  - **Day 2 回测**：需要历史 K 线，可任选其一：在【全局配置】中配置 datafeed（并安装对应包，如 `vnpy_rqdata`、`vnpy_tushare`），或先用【历史数据管理】从别处导入/录制到本地数据库。
  - **Day 3 仿真/实盘**：策略初始化时会调用 `load_bar()`，同样需要历史数据；若已连接 CTP（如 SimNow），部分接口会从交易所查询历史，否则仍需 datafeed 或本地数据库中有数据。
- **如何配置（供 Day 2 及之后使用）**：在 Trader 中打开【系统】→【全局配置】，在「数据服务」相关项中填写 `datafeed.name`（如 `rqdata`、`tushare`）及账号信息；或使用【历史数据管理】/【行情记录】先往本地数据库写入数据。配置会保存到运行目录下的 `vt_setting.json`。

---

## 验收清单（Day 1 完成标准）

- [ ] 已安装 VeighNa（Studio 或 `install.bat`），且 `import vnpy` 无报错。
- [ ] 能通过 VeighNa Station 或 `python run.py` 启动 VeighNa Trader，并看到主窗口与运行目录。
- [ ] 已将 `my_first_strategy.py` 放到运行目录下的 `strategies` 文件夹中。
- [ ] 在【功能】→【CTA策略】的策略下拉框中能看到 **MyFirstStrategy**。

全部勾选即表示 Day 1 完成，可进入 [Day 2：历史回测与参数理解](5_DAY_LIVE_TRADING_PLAN.md#day-2历史回测与参数理解)。

---

## 参考文档

- 环境安装（Windows）：[community/install/windows_install.md](community/install/windows_install.md)
- 新同学第一步策略与回测、实盘加载：[community/info/newcomer_quickstart.md](community/info/newcomer_quickstart.md)
- 5 天计划书总览：[5_DAY_LIVE_TRADING_PLAN.md](5_DAY_LIVE_TRADING_PLAN.md)
