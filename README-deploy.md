# 考研英语辅助Agent - Render部署指南

## 项目概述
这是一个基于Flask + React的考研英语学习助手，已配置好Render部署。

## 部署到Render的步骤

### 1. 准备工作
1. 确保所有文件已提交到GitHub仓库
2. 注册 [Render.com](https://render.com) 账号
3. 准备以下环境变量：
   - `OPENAI_API_KEY`: OpenAI API密钥
   - `TAVILY_API_KEY`: Tavily搜索API密钥（可选）
   - `MODEL_NAME`: 模型名称（默认：gpt-4o）
   - `API_BASE`: API基础URL（默认：https://api.deepseek.com）

### 2. 在Render上部署

#### 步骤1：创建Web Service
1. 登录Render控制台
2. 点击 "New +" → "Web Service"
3. 连接你的GitHub账户
4. 选择你的仓库：`LiMelson/postgraduate-english-assistant-agent`

#### 步骤2：配置服务
1. **名称**：`postgraduate-english-assistant`（或自定义）
2. **环境**：Python
3. **地区**：选择离你近的地区（如Singapore、Oregon等）
4. **分支**：`main`
5. **构建命令**：（已自动从render.yaml读取）
   ```
   pip install -r requirements.txt
   cd frontend && npm install && npm run build
   ```
6. **启动命令**：（已自动从render.yaml读取）
   ```
   ./start.sh
   ```

#### 步骤3：设置环境变量
在 "Environment" 标签页添加以下环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `OPENAI_API_KEY` | 你的OpenAI API密钥 | **必需** |
| `MODEL_NAME` | `gpt-4o` | 可选，默认gpt-4o |
| `API_BASE` | `https://api.deepseek.com` | 可选，默认DeepSeek |
| `TAVILY_API_KEY` | 你的Tavily API密钥 | 可选，用于搜索功能 |
| `APP_DEBUG` | `false` | 生产环境设为false |
| `APP_PORT` | `10000` | Render自动设置，无需修改 |
| `APP_HOST` | `0.0.0.0` | 必需 |

#### 步骤4：高级设置
1. **实例类型**：选择 `Free`（免费版）或 `Starter`（$7/月）
2. **自动部署**：启用（当推送到main分支时自动重新部署）
3. **健康检查路径**：`/api/health`
4. **磁盘**：添加1GB磁盘用于存储数据

#### 步骤5：部署
1. 点击 "Create Web Service"
2. Render将开始构建和部署
3. 等待部署完成（约5-10分钟）

### 3. 验证部署
1. 部署完成后，访问Render提供的URL（如 `https://postgraduate-english-assistant.onrender.com`）
2. 测试健康检查：`https://你的服务.onrender.com/api/health`
3. 测试API：`https://你的服务.onrender.com/api/ask`
4. 访问前端界面

### 4. 常见问题

#### 构建失败
1. **Python依赖安装失败**：检查requirements.txt格式
2. **Node.js构建失败**：检查frontend/package.json
3. **内存不足**：免费实例内存有限，考虑升级到付费计划

#### 应用启动失败
1. **端口绑定错误**：确保使用`$PORT`环境变量
2. **环境变量缺失**：检查所有必需环境变量
3. **导入错误**：检查Python路径和依赖

#### 性能优化
1. **启用缓存**：Render免费实例有休眠机制，首次访问较慢
2. **数据库配置**：如需数据库，使用Render PostgreSQL
3. **文件存储**：使用Render磁盘或外部存储服务

### 5. 监控和维护
1. **日志**：在Render控制台查看实时日志
2. **指标**：监控CPU、内存使用情况
3. **自动缩放**：付费计划支持自动缩放
4. **自定义域名**：可以绑定自己的域名

### 6. 更新部署
1. 推送代码到GitHub main分支
2. Render会自动重新部署
3. 或在Render控制台手动触发重新部署

## 技术支持
如有问题，请检查：
1. Render部署日志
2. 应用日志
3. 环境变量配置
4. 网络连接

祝部署顺利！