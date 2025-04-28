# filestoprompt(FTP)

> **一个能将指定文件夹内多种后缀文件合并为 AI Prompt 的小工具**，支持自定义排除或保留后缀，自动过滤常见依赖/虚拟环境目录，让你一键把项目内容变成可直接喂给 AI 的文本～

## 🔗 个人主页
- nodeseek: [https://www.nodeseek.com/space/21917#/general](https://www.nodeseek.com/space/21917#/general)

## 🚀 功能亮点
- **项目结构**：自动输出目录树，只展示你关心的文件类型
- **内容合并**：按文件顺序拼接内容，超大文件自动截断
- **后缀过滤**：  
  - `--protect-ext` 仅保留指定后缀  
  - `--exclude-ext` 排除指定后缀  
- **目录排除**：自动跳过 `env`、`.venv`、`__pycache__` 等常见目录，也可自定义
- **命令行友好**：支持输出到终端或文件

## 🎯 使用示例

# 1. 默认模式：处理 .py/.md/.ini/.env/.yaml
python ftp.py ./my_project

# 2. 排除后缀 .md/.yaml
python ftp.py ./my_project --exclude-ext .md,.yaml

# 3. 仅保留 .py/.ini
python ftp.py ./my_project --protect-ext .py,.ini

# 4. 同时排除和保留
python ftp.py ./my_project --protect-ext .py,.md --exclude-ext .md
## 📄 参数说明

| 参数            | 简述                                               | 默认值               |
| --------------- | -------------------------------------------------- | -------------------- |
| `folder`        | 要扫描的项目路径                                   | —                    |
| `-o, --output`  | 指定输出文件（不填则打印到终端）                   | —                    |
| `--max-size`    | 单文件最大读取字节（超出部分截断）                 | `1048576`（1MB）     |
| `--exclude`     | 排除目录名，多个用逗号分隔                         | `""`                 |
| `--protect-ext` | 仅保留后缀，多个用逗号分隔（e.g. `.py,.md`）        | `""`（不开启）       |
| `--exclude-ext` | 排除后缀，多个用逗号分隔（e.g. `.log,.tmp`）        | `""`（不开启）       |
