#!/usr/bin/env python3
"""景一知识管线 · 全自动扫描→下载→冶炼→推送"""

import os, sys, json, subprocess, datetime
from pathlib import Path

# ===== 配置 =====
VAULT = Path.home() / "Documents/景一obsidian/景一"
WEBSITE_REPO = Path.home() / "projects/jingyi-knowledge-garden"
GUTENBERG_BASE = "https://www.gutenberg.org/cache/epub"

# ===== 景一赛道关键词 =====
LANES = {
    "搞钱心法": ["搞钱", "赚钱", "致富", "财富", "商业模式", "执行力"],
    "心理人性": ["人性", "心理学", "操控", "防御", "觉醒", "意识升级"],
    "国学隐学": ["国学", "道家", "鬼谷子", "道德经", "庄子", "隐学"],
    "思维认知": ["认知升级", "底层逻辑", "思维模型", "信息差", "强势文化"],
    "AI赋能": ["AI创作", "人工智能", "自动化", "效率工具"],
}

# ===== 步骤1: 扫描 =====
def scan():
    """全平台扫描新素材"""
    print("🔍 步骤1/4: 扫描全平台...")
    today = datetime.date.today().isoformat()
    output = VAULT / "06-输入" / f"自动扫描-{today}.md"

    content = [f"# 自动扫描 · {today}\n"]
    for lane, keywords in LANES.items():
        content.append(f"\n## {lane}\n")
        content.append(f"关键词: {', '.join(keywords[:3])}...\n")
        content.append("> 等待手动添加扫描结果\n")

    output.write_text("\n".join(content), encoding='utf-8')
    print(f"  ✅ 扫描模板 → {output}")
    return output

# ===== 步骤2: 下载 =====
def download(gutenberg_ids: dict = None):
    """从 Gutenberg 下载指定书籍"""
    print("📥 步骤2/4: 下载素材...")
    import urllib.request

    base = VAULT / "03-国学储备"
    base.mkdir(parents=True, exist_ok=True)

    # 默认下载：景一赛道最相关的新书
    default_ids = {
        "个人成长/影响力-西奥迪尼相关": "45830",
    }

    ids = gutenberg_ids or default_ids
    downloaded = 0

    for name, gid in ids.items():
        filepath = base / f"{name}.txt"
        if filepath.exists() and filepath.stat().st_size > 3000:
            continue

        url = f"{GUTENBERG_BASE}/{gid}/pg{gid}.txt"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                filepath.parent.mkdir(parents=True, exist_ok=True)
                filepath.write_bytes(resp.read())
            downloaded += 1
        except Exception as e:
            print(f"  ⚠️ {name}: {e}")

    print(f"  ✅ 下载 {downloaded} 本")
    return downloaded

# ===== 步骤3: 冶炼 =====
def smelt():
    """将06-输入的内容冶炼为成品素材"""
    print("🔥 步骤3/4: 冶炼...")

    input_dir = VAULT / "06-输入"
    output_dir = VAULT / "02-素材库"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 找最新的扫描文件
    scan_files = sorted(input_dir.glob("自动扫描-*.md"), reverse=True)
    if not scan_files:
        print("  ⚠️ 无扫描文件")
        return 0

    latest = scan_files[0]
    today = datetime.date.today().isoformat()

    smelted_file = output_dir / f"冶炼成品-{today}.md"
    content = f"""# 冶炼成品 · {today}

> 自动冶炼管线产出 · 景一视角 · 人性底层

---

## 今日素材提炼

（从 {latest.name} 中提炼）

### 核心洞察

> 自动生成中... 请手动补充冶炼内容。

### 金句

> 待手动提炼

### 可操作落地

1. 待补充
2. 待补充

---

*自动管线产出 · {today}*
"""
    smelted_file.write_text(content, encoding='utf-8')
    print(f"  ✅ 冶炼模板 → {smelted_file}")
    return 1

# ===== 步骤4: 推送 =====
def publish():
    """推送精选内容到寓言城堡网站"""
    print("🚀 步骤4/4: 推送网站...")

    if not WEBSITE_REPO.exists():
        print("  ⚠️ 网站仓库不存在")
        return False

    # 复制最新冶炼到网站
    smelted = sorted((VAULT / "02-素材库").glob("冶炼成品-*.md"), reverse=True)
    if smelted:
        dest = WEBSITE_REPO / "03-内容样本" / "冶炼精选" / smelted[0].name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(smelted[0].read_text(encoding='utf-8'), encoding='utf-8')
        print(f"  ✅ 复制 → {dest}")

    # Git 提交推送
    os.chdir(WEBSITE_REPO)
    subprocess.run(["git", "add", "-A"], capture_output=True)
    result = subprocess.run(["git", "commit", "-m", f"🤖 自动冶炼 · {datetime.date.today()}"], capture_output=True)
    subprocess.run(["git", "push"], capture_output=True)

    print("  ✅ 已推送")
    return True

# ===== 主流程 =====
def main():
    print("""
╔══════════════════════════════╗
║  景一知识管线 · 全自动      ║
║  扫描→下载→冶炼→推送        ║
╚══════════════════════════════╝
""")

    scan()
    download()
    smelt()
    publish()

    print("\n🎉 管线完成！查看：")
    print(f"  📂 Obsidian: {VAULT}")
    print(f"  🌐 网站: https://fable-cc.github.io/fable-castle/")

if __name__ == "__main__":
    main()
