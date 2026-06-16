#!/usr/bin/env python3
"""Obsidian → GitHub 知识蒸馏管道"""

import os, sys, re, json, subprocess
from pathlib import Path
from datetime import datetime

OBSIDIAN_VAULT = Path.home() / "Documents/景一obsidian/景一"
GITHUB_REPO = Path.home() / "projects/jingyi-knowledge-garden"
PILLAR_DIR = GITHUB_REPO / "02-知识图谱"
STATE_FILE = Path.home() / ".claude/projects/-Users-jingyi/distillation_state.json"

# Mapping from Obsidian content patterns to GitHub pillars
PILLAR_MAP = {
    "搞钱|钱途|商业|财富|变现|执行力|转运|情商|人情": "钱途心法",
    "隐学|信息封锁|强势|权力|博弈|规则|暗流|秘术": "暗流规则",
    "觉醒|NPC|维度|意识|降权|系统|升级|真人": "意识觉醒",
    "斯多葛|道家|尼采|庄子|佛学|禅宗|东西|比较|哲学": "东学西渐",
    "荣格|弗洛伊德|阿德勒|詹姆斯|心理学|人格|原型|驱力": "深度心理学",
    "韩非|马基雅维利|孙子|克劳塞维茨|博弈|策略|制度": "权力策略",
    "模式|画布|护城河|股权|轻资产|增长|盈利|飞轮": "模式设计",
    "认知|偏差|卡尼曼|塞勒|决策|思维模型|系统1": "认知重构",
    "说服|影响力|品牌|叙事|营销|传播|修辞|西奥迪尼": "人性说服",
    "历史|文明|帝国|周期|技术变革|汤因比|戴蒙德": "文明规则",
    "深度工作|多巴胺|习惯|注意力|能量|巅峰|休伯曼": "能量管理",
    "易经|黄帝内经|丹道|王阳明|杨朱|心身|风水": "隐学意识",
    "纳瓦尔|芒格|彼得森|达利欧|塔勒布": "全球大V",
}

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"processed": [], "last_run": None}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

def classify_content(title, content):
    """Classify content into a pillar based on keyword matching."""
    text = title + " " + content[:500]
    for pattern, pillar in PILLAR_MAP.items():
        if re.search(pattern, text):
            return pillar
    return "钱途心法"  # default

def smelt_content(title, content, pillar):
    """Transform raw Obsidian content into 景一-style pillar article."""
    # Basic smelting: add frontmatter, structure, remove noise
    lines = content.strip().split("\n")

    # Extract key sentences (non-empty, non-header, substantial)
    key_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith(">"):
            continue
        if len(line) > 15 and len(line) < 200:
            key_lines.append(line)

    # Build smelted article
    slug = re.sub(r'[^\w\s-]', '', title[:30]).strip().lower().replace(' ', '-')
    filename = f"{pillar}-{slug}.md"

    frontmatter = f"""---
source: 景一冶炼·Obsidian蒸馏
date: {datetime.now().strftime('%Y-%m-%d')}
tags: [{pillar}]
pillar: {pillar}
---

# {title}

## 核心论点

{key_lines[0] if key_lines else title}

---

## 关键论述

"""
    body = "\n".join(f"- {l}" for l in key_lines[1:10]) if len(key_lines) > 1 else ""

    return filename, frontmatter + body

def scan_obsidian():
    """Scan Obsidian for new content to distill."""
    files = []
    for root, dirs, filenames in os.walk(OBSIDIAN_VAULT):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in filenames:
            if f.endswith('.md') and not f.startswith('.'):
                files.append(Path(root) / f)
    return files

def main():
    state = load_state()
    print(f"📊 状态: {len(state['processed'])} 篇已处理, 上次: {state.get('last_run', '首次')}")

    # Scan
    all_files = scan_obsidian()
    print(f"📁 Obsidian 总文件: {len(all_files)}")

    # Find new files
    new_files = [f for f in all_files if str(f) not in state['processed']]
    print(f"🆕 新文件: {len(new_files)}")

    if not new_files:
        print("✅ 无需处理")
        return

    # Process (limit to 10 per run)
    to_process = new_files[:10]
    distilled = 0
    skipped = 0

    for filepath in to_process:
        try:
            content = filepath.read_text(encoding='utf-8')
            title = filepath.stem

            # Skip templates, scans, short files, trash
            if title.startswith('_') or title.startswith('.'):
                state['processed'].append(str(filepath))
                skipped += 1
                continue
            if '扫描' in title or '模板' in title:
                state['processed'].append(str(filepath))
                skipped += 1
                continue
            if len(content) < 300:
                state['processed'].append(str(filepath))
                skipped += 1
                continue
            # Skip pure list/directory files
            if content.count('\n- ') > len(content) / 80:
                state['processed'].append(str(filepath))
                skipped += 1
                continue

            pillar = classify_content(title, content)
            filename, article = smelt_content(title, content, pillar)

            output_path = PILLAR_DIR / filename
            if not output_path.exists():
                output_path.write_text(article, encoding='utf-8')
                distilled += 1
                print(f"  ✅ [{pillar}] {filename}")

            state['processed'].append(str(filepath))
        except Exception as e:
            print(f"  ⚠️ {filepath.name}: {e}")

    state['last_run'] = datetime.now().isoformat()
    save_state(state)

    print(f"\n🔥 蒸馏完成: {distilled} 篇新文章")

    # Push to GitHub if there are changes
    if distilled > 0:
        os.chdir(GITHUB_REPO)
        subprocess.run(["git", "add", "-A"])
        result = subprocess.run(["git", "commit", "-m", f"🔥 Obsidian蒸馏: {distilled}篇新文章"],
                              capture_output=True, text=True)
        if "nothing to commit" not in result.stdout + result.stderr:
            subprocess.run(["git", "push"])
            print("✅ 已推送到 GitHub")

if __name__ == "__main__":
    main()
