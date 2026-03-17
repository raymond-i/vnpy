# Day 3：SimNow 仿真与策略实盘形态验证（具体步骤）

本文为《VeighNa 入门到实盘 5 天计划书》Day 3 的可执行步骤说明，目标是用 SimNow CTP 仿真连接 Trader，在「实盘形态」下跑同一策略（初始化 → 启动 → 看日志与持仓），不追求盈利，只验证流程。

---

## 目标与产出

- **目标**：用 SimNow CTP 仿真连接 Trader，在实盘形态下完成策略的初始化与启动，验证从连接到策略运行的完整流程。
- **产出**：SimNow 下策略从初始化到运行的完整流程跑通；日志无「行情订阅失败」等错误；若有简单开平逻辑，能看到委托/成交/持仓变化。

---

## 前置条件

- 已完成 [Day 1](DAY1_环境与第一个CTA策略_步骤.md)（环境与 MyFirstStrategy 可加载）和 [Day 2](DAY2_历史回测与参数理解_步骤.md)（可选，建议至少跑过一次回测熟悉合约与参数）。
- 需安装 **vnpy_ctp**（CTP 交易接口）。若使用本仓库 `.venv`，可执行：`pip install vnpy_ctp`。
- 启动 Trader 时需加载 CTP 与 CTA 策略模块（使用 [examples/veighna_trader/run.py](../examples/veighna_trader/run.py) 时已包含；若用 run_day1.py 需改用 run.py 以连接 CTP）。

---

## 步骤一：获取 SimNow 仿真账号

1. 打开 [SimNow 官网](http://www.simnow.com.cn/)，使用手机号注册并登录。
2. 在 SimNow 后台获取：
   - **用户名（InvestorID）**：6 位纯数字（非注册手机号）。
   - **密码**：首次使用前需在 SimNow 修改一次密码，修改后的密码用于 VeighNa 连接。
3. 在 [SimNow 产品页](http://www.simnow.com.cn/product.action) 获取当前可用的：
   - **经纪商代码**：SimNow 为 **9999**。
   - **交易服务器**、**行情服务器**：分为「盘中」与「盘后」两套，地址与端口以产品页为准（例：盘中 7x24 环境、盘后测试环境，适用时间段不同）。
4. 详见 [gateway - CTP](community/info/gateway.md)。

---

## 步骤二：在 Trader 中连接 CTP（SimNow）

1. 启动 VeighNa Trader（通过 VeighNa Station 或 `run.py`，确保已加载 CTP 与 CTA 策略）。
2. 菜单栏点击【系统】→【连接 CTP】，弹出配置窗口。
3. 按 SimNow 要求填写（以常见示例为准，具体以 SimNow 产品页为准）：
   - **用户名**：6 位 InvestorID。
   - **密码**：在 SimNow 修改后的密码。
   - **经纪商代码**：9999。
   - **交易服务器** / **行情服务器**：从 SimNow 产品页复制（如盘中：`180.168.146.187:10201` / `180.168.146.187:10211`，以官网为准）。
   - **产品名称**：如 `simnow_client_test`。
   - **授权编码**：如 16 个 0。
4. 点击【连接】。
5. **验收**：在 Trader 主界面【日志】中看到登录成功、**「合约信息查询成功」** 等输出；【账户】、【持仓】等组件有数据或为空但无报错。若长时间无输出，可用 telnet 检查交易/行情端口是否可达。

参考：[VeighNa Trader - SimNow](community/info/veighna_trader.md)。

---

## 步骤三：加载并运行策略

1. 打开【功能】→【CTA策略】。
2. 若尚未添加该合约的策略实例：
   - 策略下拉框选择 **MyFirstStrategy**，点击【添加策略】。
   - **实例名称**：任意不重名名称（如 `my_first_simnow`）。
   - **合约品种（vt_symbol）**：与 Day 1 / Day 2 一致，且为 SimNow 支持的合约，如 `IF888.CFFEX`、`rb2505.SHFE`（必须带交易所后缀）。
   - 参数可保持默认，点击【添加】。
3. 在左侧策略列表中选中该实例，先点击【初始化】，等待初始化完成（日志中会有「策略初始化」、可能还有 load_bar 相关提示；若此前未配置 datafeed，会有「查询K线数据失败」但仍会完成初始化）。
4. 初始化完成后，点击【启动】。
5. **验收**：
   - 日志中无 **「行情订阅失败，找不到合约 xxx」**（若出现，多为合约代码错误或未连接 CTP/合约未在 SimNow 挂牌）。
   - 若有简单开平逻辑，可在【委托】、【成交】、【持仓】中观察变化；若为仅计算均线的演示策略，可观察日志与策略变量刷新。

详见 [newcomer_quickstart 第三步](community/info/newcomer_quickstart.md)。

---

## 可选：PaperAccount 本地仿真

若希望先用「本地仿真」练手（不连 SimNow，用实盘行情本地撮合），可安装并加载 [PaperAccount](community/app/paper_account.md)，在连接行情源后使用本地模拟下单；熟悉流程后再在 Trader 中连接 SimNow，按上述步骤三加载同一策略。

---

## 常见问题

- **行情订阅失败，找不到合约**：确认 (1) 已连接 CTP 且日志有「合约信息查询成功」；(2) vt_symbol 与交易所匹配且为 SimNow 支持的合约（如 IF888.CFFEX）；(3) 合约代码与【帮助】→【合约查询】中一致。
- **查询K线数据失败：没有正确配置数据服务**：策略初始化时会 load_bar，若未配置 datafeed，会报此提示；初始化仍会完成，实盘运行依赖 Tick 合成 K 线。若希望初始化阶段也有历史 K 线，需配置 datafeed 或提前在本地数据库中有数据。
- **连接 CTP 后无日志**：检查交易/行情服务器地址与端口是否正确、网络是否可达；SimNow 两套环境（盘中/盘后）适用时间段不同，需选对当前可用的环境。

---

## 验收清单（Day 3 完成标准）

- [ ] 已注册 SimNow 并获取 InvestorID、密码、经纪商 9999、交易/行情服务器地址。
- [ ] 在 Trader 中【系统】→【连接 CTP】成功，日志出现「合约信息查询成功」。
- [ ] 在【CTA策略】中添加 MyFirstStrategy 实例，vt_symbol 填写正确且为 SimNow 支持合约。
- [ ] 对该实例执行【初始化】与【启动】，日志无「行情订阅失败」；若有交易逻辑，能在委托/成交/持仓中看到变化。

---

## 下一步

完成 Day 3 后，可进入 [Day 4：风控、实盘准备与检查清单](5_DAY_LIVE_TRADING_PLAN.md#day-4风控实盘准备与检查清单)。

---

## 参考文档

- [gateway - CTP / SimNow](community/info/gateway.md)
- [VeighNa Trader - SimNow 连接](community/info/veighna_trader.md)
- [新同学入门 - 第三步 实盘/模拟加载](community/info/newcomer_quickstart.md)
- [CTA策略](community/app/cta_strategy.md)
- [5 天计划书 - Day 3](5_DAY_LIVE_TRADING_PLAN.md#day-3simnow-仿真与策略实盘形态验证)
