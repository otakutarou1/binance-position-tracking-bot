# 熬鹰资本持仓跟踪配置

本仓库 Fork 自 hgnx/binance-position-tracking-bot，保留原始排行榜程序；新增跟单组合数据检查。**尚未启用实时持仓提醒。**

## 已配置目标
名称：熬鹰资本
组合 ID：5075281354358777856
主页：https://www.binance.com/zh-CN/copy-trading/lead-details/5075281354358777856

## 实测结果（2026-11-14 UTC）
GitHub Actions 无登录测试：组合名称验证通过、详情和持仓请求成功，但详情 positionShow=false、持仓 data=[]。
这代表当前匿名访问不能确认真实仓位，不能当成空仓，不能产生平仓提醒。
首次检查只验证请求/身份；后续修正为同时验证持仓公开开关，未公开时检查应失败。

## 文件
- tracked_portfolios.json：目标列表，新增 KOL 添加一条包含 name、portfolio_id、url 的记录。组合 ID 必须保存为字符串。
- probe_copy_trading.py：逐个校验目标身份、接口响应和持仓可见性。
- Actions → Check KOL public data：手动检查，诊断输出保留 3 天。没有定时持续运行。
- main.py：上游排行榜程序，需要 encryptedUid；不要把跟单组合 ID 填入。

## 下一步
需要该组合公开持仓，或本人/平台提供合法授权的数据访问方式；不能保证登录即可查看。
确认可见后才能验证真实字段并实现快照比较、持久化、去重及开/加/减/平仓事件。
持续服务建议使用常驻容器，配置目标列表共享核心逻辑、每个组合独立保存状态。
通知可使用 Telegram，凭据通过环境变量 TELEGRAM_BOT_TOKEN、TELEGRAM_CHAT_ID 注入，不写入 Git。
不需要交易/提现权限；本仓库没有自动下单配置。
