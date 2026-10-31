"""ArchivalEra（GitHub profile 仓）的事实采集层。

⚠️ 本仓是 **profile 仓**：README.md 直接渲染在 https://github.com/ArchivalEra 主页上。
它不是软件项目，所以上游那个数 py/md 的 `measure_example()` 毫无意义。

本仓要量的是**主页资产的完整性**：卡片文件在不在、README 有没有引用它、
卡片源（SVG）与渲染产物（PNG）是否成对。
"""

import os

import sys as _sys

_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gate import module_meta                               # noqa: E402
from ledger import fact                                    # noqa: E402

ROOT = os.getcwd()


def _exists(rel):
    return 1 if os.path.exists(os.path.join(ROOT, rel)) else 0


def measure():
    facts = {}

    # ── 卡片资产是否成对（src 改了却忘了重渲染 = 主页显示旧图）──────────────
    facts["card_svg"] = fact(
        _exists("card/card.svg"),
        "test -f card/card.svg && echo 1 || echo 0",
        "card/card.svg",
        "卡片矢量源（可编辑的真相源）",
    )
    facts["card_png"] = fact(
        _exists("card/card.png"),
        "test -f card/card.png && echo 1 || echo 0",
        "card/card.png",
        "卡片渲染产物（主页实际显示的那张）",
    )

    # ── README 是否引用了卡片（profile 仓的全部价值就在这一行）────────────────
    readme = ""
    try:
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = fh.read()
    except OSError:
        pass
    facts["readme_refs_card"] = fact(
        1 if ("card.svg" in readme or "card.png" in readme) else 0,
        "grep -qE 'card\\.(svg|png)' README.md && echo 1 || echo 0",
        "README.md",
        "README 是否引用了卡片（profile 仓的唯一功能就是这条引用）",
    )

    # ── README 里外部图床依赖数（越少越不易碎）────────────────────────────────
    import re
    n_ext = len(re.findall(r"\]\((https?://[^)]+)\)", readme))
    facts["readme_external_links"] = fact(
        n_ext,
        "python3 -c \"import re;t=open('README.md',encoding='utf-8').read();print(len(re.findall(r'\\]\\((https?://[^)]+)\\)',t)))\"",
        "README.md",
        "README 里的外部链接数（含图片与普通链接；外链越多主页越依赖别人的可用性）",
    )

    return facts


MODULE = module_meta(
    "本仓数据层",
    "量 profile 主页资产：卡片成对性 / README 引用 / 外链数",
    selftest=False,
)
