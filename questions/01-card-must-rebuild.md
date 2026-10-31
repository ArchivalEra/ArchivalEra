# 01: 改 card.svg 后必须重新渲染 card.png（否则主页显示旧图）

**What to build:** 一条自动校验——`card/card.png` 的 mtime 不早于 `card/card.svg`。早于就是「改了源忘了重渲染」。

**为什么挂这条**：profile 仓的主页显示的是 `card.png`（README 引用它），而 `card.svg` 才是可编辑的源。
两者不同步时，**主页会静默显示上一版卡片**——没有任何报错，只有肉眼能发现。

**Settling:** 不存在 —— **第一交付物就是这条判据本身**（可放进 pre-commit 或一个 `check_card_fresh.py`）。
判据：`test card/card.png -nt card/card.svg` 的 rc=0。

**Status:** ready-for-agent
