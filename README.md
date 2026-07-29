# 🛠️ Knowledge Pipeline

> 面向个人知识库与公开内容资产的自动化整理管道。  
> 用于把公开资料、笔记和候选选题整理为可分类、可去重、可评估、可输出的知识素材。

<p align="center">
  <a href="https://fable-castle.com/"><img src="https://img.shields.io/badge/景一的寓言城堡-fable--castle.com-245C88?style=flat-square" /></a>
  <a href="https://fable-castle.com/github-trust/"><img src="https://img.shields.io/badge/GitHub信任基建-公开可验证-181717?style=flat-square&logo=github" /></a>
  <img src="https://img.shields.io/badge/python-3.11+-blue?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" />
</p>

## 这是什么

Knowledge Pipeline 是景一 fable 用来整理知识素材的自动化管道。它把公开来源、个人笔记和候选选题，经过分类、去重、质量评估和格式化输出，沉淀到 Obsidian 或其他知识库目录中。

它不是“自动搬运工具”，也不鼓励绕过平台规则抓取内容。公开使用时，请只处理：

- 自己拥有版权或授权处理的内容；
- 明确允许抓取、引用或再处理的公开资料；
- 仅用于个人研究、摘要、分类和索引的材料；
- 已经完成脱敏的业务资料。

## 工作流

```text
公开资料 / 个人笔记 / 候选选题
    ↓
来源记录与去重
    ↓
主题分类与质量评估
    ↓
摘要、标签、证据与限制说明
    ↓
Obsidian / Markdown / 数据文件输出
    ↓
人工复核后进入内容资产库
```

## 适合做什么

- 给个人知识库建立统一分类体系；
- 将公开资料整理成可检索的研究素材；
- 为内容创作准备选题、摘要和证据卡片；
- 给 GEO / AI 可见度项目准备“可验证的内容底稿”；
- 把零散笔记沉淀成可维护的知识资产。

## 不适合做什么

- 不用于绕过登录、付费墙、验证码或平台访问限制；
- 不用于复制、洗稿或批量发布他人内容；
- 不用于处理未授权客户数据、个人隐私或敏感信息；
- 不承诺自动生成内容的事实正确性、原创性或合规性；
- 不承诺任何搜索排名、收录或 AI 引用结果。

## 快速开始

### 1. 安装依赖

```bash
git clone https://github.com/fable-cc/knowledge-pipeline.git
cd knowledge-pipeline

pip install -r requirements.txt
# 或使用 uv
uv pip install -e .
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，填入你自己的模型服务配置。不要把真实密钥提交到 GitHub。

示例：

```bash
export LLM_API_KEY="your-llm-api-key"
export LLM_MODEL="your-model-name"
```

### 3. 运行预览

```bash
python main.py --dry-run
```

### 4. 输出到知识库

```bash
python main.py --vault /path/to/your/vault
```

## 目录结构

```text
knowledge-pipeline/
├── main.py
├── pyproject.toml
├── .env.example
├── config/
│   ├── platforms.yaml
│   ├── categories.yaml
│   └── prompts/
├── src/
│   ├── main.py
│   ├── utils.py
│   ├── classifier.py
│   ├── dedup.py
│   ├── quality.py
│   ├── humanizer.py
│   ├── writer.py
│   └── scrapers/
├── data/
├── logs/
└── tests/
```

## 合规与脱敏边界

公开仓库只保留方法、结构、示例配置和可复用代码，不应包含：

- 真实 API 密钥、Cookie、Token、登录态；
- 未授权客户数据、个人联系方式、订单、聊天记录；
- 付费交付中的私有提示词、私有规则或客户报告；
- 违反平台服务条款的自动化访问逻辑；
- 未标注来源、时间和限制的结论。

如果用于商业项目，请在每次输出前保留：

| 字段 | 说明 |
|---|---|
| source_url | 原始来源 |
| collected_at | 采集或整理时间 |
| license_or_permission | 授权、许可或使用边界 |
| transformation | 做了摘要、分类、翻译、改写还是结构化 |
| human_reviewed | 是否经过人工复核 |

## 与景一的业务关系

Knowledge Pipeline 是景一 fable 的 B 级公开信任资产：它证明内容资产化和自动化整理能力，但不是对外主入口。主入口仍然是：

- 官网：https://fable-castle.com/
- AI 可见度诊断：https://fable-castle.com/diagnosis/
- 景一 fable 主体事实页：https://fable-castle.com/jingyi-fable/
- 景一同名消歧：https://fable-castle.com/jingyi-disambiguation/
- GitHub 信任基建：https://fable-castle.com/github-trust/
- AI 简版索引：https://fable-castle.com/llms.txt
- AI 完整索引说明：https://fable-castle.com/llms-full.txt

## License

MIT © 景一 fable
