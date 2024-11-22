# GitHub to LLM

一个将 GitHub 仓库代码转换为结构化文档的工具，支持多种代码获取方式，便于进行后续的 LLM (大语言模型) 处理。

## 功能特点

- 🔄 支持多种代码获取方式
  - HTTP API 方式：适合小型仓库，无需下载完整代码
  - Clone 方式：适合大型仓库，本地处理更快
  - 可通过配置文件或界面动态切换

- 📁 智能文件处理
  - 自动过滤二进制文件
  - 可配置的文件排除规则
  - 支持多种编程语言

- 📊 结构化输出
  - 生成清晰的目录树
  - 代码块带有语言标识
  - 支持 Markdown 格式输出

- 🎨 现代化 Web 界面
  - 实时处理进度展示
  - 支持复制和下载结果
  - 响应式设计，支持移动端

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

创建或修改 `config/default_config.yml`:

```yaml
github_handler:
  mode: "http"  # 可选值: "http" 或 "clone"
  shallow_clone: true  # 是否使用浅克隆

exclude_patterns:
  - "**/__pycache__/**"
  - "**/.git/**"
  
exclude_extensions:
  - ".pyc"
  - ".pyo"
  - ".pyd"

exclude_files:
  - "LICENSE"
  - "poetry.lock"
```

### 运行

```bash
python -m repo2llm.app
```

访问 `http://localhost:5000` 开始使用。

## 使用方法

1. 在网页界面输入 GitHub 仓库 URL
2. 选择代码获取方式（可选）：
   - 默认：使用配置文件中的设置
   - 克隆：克隆整个仓库到本地处理
   - HTTP：使用 GitHub API 获取文件
3. 点击"处理"按钮
4. 等待处理完成，查看生成的文档
5. 可以复制或下载生成的 Markdown 文件

## 项目结构

```
githubtoLLM/
├── config/
│   └── default_config.yml     # 默认配置文件
├── src/
│   └── repo2llm/
│       ├── app.py            # Web 应用主程序
│       ├── github_handler.py # GitHub 代码获取处理
│       ├── main.py          # 核心逻辑
│       ├── markdown_converter.py # Markdown 转换
│       └── static/          # 静态资源
│           ├── css/         # 样式文件
│           └── js/          # JavaScript 文件
├── output/                  # 输出目录
│   └── cloned_repos/       # 克隆的仓库存储位置
└── requirements.txt        # 项目依赖
```

## 依赖项

- Python 3.7+
- Flask
- GitPython
- PyYAML
- Requests

## 配置说明

### GitHub 处理器配置

- `mode`: 代码获取方式
  - `http`: 使用 GitHub API 获取文件（适合小型仓库）
  - `clone`: 克隆仓库到本地（适合大型仓库）
- `shallow_clone`: 是否使用浅克隆（仅克隆最新版本）

### 文件过滤配置

- `exclude_patterns`: 要排除的文件路径模式
- `exclude_extensions`: 要排除的文件扩展名
- `exclude_files`: 要排除的具体文件名

## 注意事项

1. 使用 HTTP 模式时，请注意 GitHub API 的访问限制
2. 克隆模式需要足够的磁盘空间
3. 对于私有仓库，需要配置 GitHub Token
4. 建议根据仓库大小选择合适的获取方式

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
