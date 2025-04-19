🛰️ EchoWatch - 开发日志与洞察记录 | Development Log & Insights
记录 EchoWatch 从一个模糊的念头到具体实现的全过程。它并不源于某个新闻，也不是因为看到什么具体威胁，而只是一个问题在我脑中回响：
This log captures how EchoWatch evolved from a vague thought into a working system. It wasn’t inspired by a specific incident, but by a question that echoed in my mind:

“如果我们能在悲剧发生前察觉一些蛛丝马迹，会不会有人因此得救？”
“If we could spot a pattern before the tragedy happens, could someone be saved?”

灵感来自电影《少数派报告》（Minority Report）——但我们不用预言，而用公共数据与AI，构建“数字巡逻系统”。
Inspired by Minority Report — but instead of psychics, we use open data and AI to create a digital patrol system.

🧠 初衷 | Motivation
我没看到什么具体威胁或恐吓，只是脑海中突然冒出一个问题：
I didn’t see any specific threat or attack. I just had a sudden thought:

“如果悲剧之前总有征兆，我们能否早点看见？”
“If tragedy leaves clues, could we catch them early?”

于是我决定试试看。
So I decided to try.

🛠️ 开发历程 | Development History
v0.1: Reddit 关键词匹配测试
→ Basic Reddit keyword matching prototype

v0.3: Pastebin 接入，但误报多
→ Integrated Pastebin scanning (high false positives)

v0.4: GPT 审查模块测试接入
→ GPT-assisted intent scoring (test mode only)

v0.5: 全面升级关键词，转向“意图型表达”
→ Upgraded to intent-style trigger phrases

v0.6: 接入 4plebs 爬虫，绕过 403
→ 4plebs headless browser scraper added (via Selenium)

🧪 当前问题 | Known Issues
🔁 关键词匹配效率低，误报多，漏报也多
→ Keyword search is rigid and imprecise

打算接入 GPT 模型改为语义理解，但目前没有 API 预算。
→ Plan to use GPT for semantic scoring, but no budget right now.

🔒 Discord 和 Telegram 私密社区无法接入
→ Many high-risk communities are private and inaccessible

目前只能扫描公开频道，但也许这就足够了。
→ For now, scanning public data might already be useful.

🔮 下一步计划 | Roadmap
📄 每日威胁摘要输出（HTML/PDF）
→ Generate daily summary reports

🧠 集成 GPT 模块辅助评分
→ Add GPT scoring to improve threat precision

🛰️ Telegram 公共频道监听
→ Start scanning public Telegram channels

📦 threat_log 日志推送功能（网页/邮箱）
→ Enable web/email log delivery system

💬 思考记录 | Reflections
“钓不到鱼，并不代表海里没鱼，只是你还不够久。”
“You’re not failing to catch fish. You just haven’t waited long enough.”

“我希望这个工具永远抓不到真正的威胁。”
“Ideally, this tool never actually catches a real threat.”

“能不能让 AI 做正义的一方？”
“What if AI could be the one enforcing public safety?”

“有些工具不是为了赚钱而造，是为了守住底线。”
“Some tools aren’t built for profit. They’re built to protect the edge.”

👨‍💻 作者 | Author
Alex Tang
加拿大软件工程师 / 数字公益探索者 / EchoWatch 项目开发者
Canadian software developer / Digital safety advocate / Creator of EchoWatch

GitHub → https://github.com/PacificZenA/EchoWatch