# 配置文件
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'env', '.env'))

# 搜索引擎配置
SEARCH_CONFIG = {
    "tavily_api_key": os.getenv("TAVILY_API_KEY", "your_tavily_api_key_here"),
    "max_results": 5,
    "search_depth": "deep"
}

# 大模型API配置
LLM_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY", "YOUR_API_KEY"),  # 从环境变量读取API密钥
    "model": os.getenv("MODEL_NAME", "gpt-4o"),  # 从环境变量读取模型名称
    "temperature": 0.7,  # 温度参数
    "max_tokens": 2000,  # 最大token数
    "api_base": os.getenv("API_BASE", "https://api.deepseek.com")  # 从环境变量读取API基础URL
}

# 应用配置
APP_CONFIG = {
    "debug": os.getenv("APP_DEBUG", "true").lower() == "true",  # 调试模式
    "port": int(os.getenv("APP_PORT", "5000")),  # 服务端口
    "host": os.getenv("APP_HOST", "0.0.0.0")  # 服务主机
}

# 知识点提取配置
KNOWLEDGE_EXTRACTOR_CONFIG = {
    "min_keyword_length": 2,  # 关键词最小长度
    "max_keywords": 50,  # 最大关键词数
    "stop_words_file": "app/tools/utils/stop_words.txt"  # 停用词文件
}

# 思维导图生成配置
MINDMAP_CONFIG = {
    "output_dir": "app/data/mindmaps",  # 输出目录
    "max_depth": 3,  # 最大深度
    "max_children": 5  # 每个节点最大子节点数
}

# 全局设置类
class Settings:
    def __init__(self):
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "your_tavily_api_key_here")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
        self.MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
        self.API_BASE = os.getenv("API_BASE", "https://api.deepseek.com/v1")
        self.APP_DEBUG = os.getenv("APP_DEBUG", "true").lower() == "true"
        self.APP_PORT = int(os.getenv("APP_PORT", "5000"))
        self.APP_HOST = os.getenv("APP_HOST", "0.0.0.0")

# 创建全局设置实例
settings = Settings()
