---
title: 考研英语辅助Agent
description: 基于人工智能的考研英语学习助手，旨在帮助考研学生提高英语学习效率和成绩
---

# 考研英语辅助Agent

## 项目简介

考研英语辅助Agent是一个基于人工智能的考研英语学习助手，旨在帮助考研学生提高英语学习效率和成绩。它能够智能识别用户的问题类型，并根据问题类型提供相应的回答和学习资源。

## 核心功能

- **智能问题分类**：能够识别用户的问题类型，区分问候语和考研英语相关问题
- **考研英语真题搜索**：能够搜索和提供考研英语真题及解析
- **智能对话**：能够进行自然语言对话，回答用户的各种问题
- **会话记忆**：能够记住对话历史，提供连贯的对话体验
- **流式输出**：能够实时显示AI的回答过程，提升用户体验

## 技术栈

- **后端**：Python, Flask, LangGraph, OpenAI API
- **前端**：React, Vite, Tailwind CSS
- **工具**：LangGraph（工作流管理）, OpenAI API（语言模型）, Flask-CORS（跨域请求）

## 项目结构

```
考研英语辅助Agent/
├── app/                 # 后端应用
│   ├── api/             # API路由
│   ├── graph/           # 工作流管理
│   ├── models/          # 数据模型
│   ├── services/        # 服务层
│   ├── tools/           # 工具类
│   ├── __init__.py
│   └── main.py          # 后端入口
├── config/              # 配置文件
├── env/                 # 环境变量
├── frontend/            # 前端应用
│   ├── src/             # 前端源码
│   ├── index.html
│   └── package.json     # 前端依赖
├── .gitignore
├── README.md            # 项目说明
└── requirements.txt     # 后端依赖
```

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 16+

### 安装步骤

1. **克隆项目**

```bash
git clone <项目仓库地址>
cd 考研英语辅助Agent
```

2. **安装后端依赖**

```bash
pip install -r requirements.txt
```

3. **安装前端依赖**

```bash
cd frontend
npm install
```

4. **配置环境变量**

在 `env/.env` 文件中配置 OpenAI API 密钥：

```
OPENAI_API_KEY=your_api_key_here
```

5. **启动后端服务**

```bash
# 在项目根目录下运行
python app/main.py
```

6. **启动前端服务**

```bash
# 在 frontend 目录下运行
npm run dev
```

7. **访问应用**

打开浏览器，访问 `http://localhost:5173` 即可使用应用。

## API 接口

### POST /api/process

处理用户问题，智能判断是直接回答还是搜索（流式输出）。

**请求参数**：
- `question`：用户问题
- `conversation_id`：会话ID（可选，默认值："default"）

**响应格式**：

```json
{
  "type": "search" || "direct",
  "content": {
    "explanation": "回答内容",
    "original_question": "原始问题" (仅在 direct 类型时返回),
    "mindmap_path": "思维导图路径" (仅在 direct 类型时返回)
  }
}
```

### POST /api/ask

处理用户问题，返回完整回答。

**请求参数**：
- `question`：用户问题

**响应格式**：

```json
{
  "explanation": "回答内容",
  "question": "原始问题",
  "keywords": ["关键词1", "关键词2"],
  "mindmap_path": "思维导图路径"
}
```

## 工作原理

1. **问题分类**：通过关键词匹配和LLM分类，将用户问题分为问候语、考研英语相关问题和无意义内容。
2. **路由处理**：根据问题类型，将请求路由到不同的处理节点。
3. **内容生成**：根据问题类型，生成相应的回答内容。
4. **会话管理**：使用LangGraph的InMemorySaver实现会话记忆，提供连贯的对话体验。
5. **流式输出**：通过流式API，实时显示AI的回答过程，提升用户体验。

## 功能特点

- **智能分类**：能够智能识别用户的问题类型，提供相应的回答。
- **实时反馈**：通过流式输出，实时显示AI的回答过程。
- **会话记忆**：能够记住对话历史，提供连贯的对话体验。