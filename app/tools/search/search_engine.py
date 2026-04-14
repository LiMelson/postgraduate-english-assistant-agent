#!/usr/bin/env python3
"""
搜索引擎集成模块
功能：集成Tavily搜索引擎，实现全网搜索功能
"""
import requests
import os
from config.settings import settings

class SearchEngine:
    def __init__(self):
        """初始化搜索引擎"""
        self.api_key = settings.TAVILY_API_KEY
        self.base_url = "https://api.tavily.com/search"
    
    def search(self, query, num_results=5):
        """
        搜索相关内容
        
        Args:
            query: 搜索查询
            num_results: 结果数量
            
        Returns:
            搜索结果列表
        """
        if not self.api_key or self.api_key == "your_tavily_api_key_here":
            print("警告: Tavily API密钥未配置，请在env/.env文件中设置TAVILY_API_KEY")
            return []
        
        try:
            params = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": "deep",
                "topic": "education",
                "max_results": num_results
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])
            
            # 处理搜索结果
            processed_results = []
            for result in results:
                processed_result = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "score": result.get("score", 0)
                }
                processed_results.append(processed_result)
            
            return processed_results
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def search_kaoyan_english(self, query, num_results=5):
        """
        搜索考研英语相关内容
        
        Args:
            query: 搜索查询
            num_results: 结果数量
            
        Returns:
            搜索结果列表
        """
        # 构建更精确的搜索查询
        enhanced_query = f"考研英语 {query} 真题 解析"
        return self.search(enhanced_query, num_results)
