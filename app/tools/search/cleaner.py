#!/usr/bin/env python3
"""
搜索结果清理模块
功能：清理和规范化搜索结果，提取有用信息
"""
import re
from app.tools.utils.text_processor import TextProcessor

class ResultCleaner:
    def __init__(self):
        """初始化清理器"""
        self.text_processor = TextProcessor()
    
    def clean_result(self, result):
        """
        清理单个搜索结果
        
        Args:
            result: 搜索结果字典
            
        Returns:
            清理后的结果
        """
        if not result:
            return {}
        
        # 清理标题
        title = result.get("title", "")
        cleaned_title = self._clean_text(title)
        
        # 清理内容
        content = result.get("content", "")
        cleaned_content = self._clean_text(content)
        
        # 提取知识点
        knowledge_points = self._extract_knowledge_points(cleaned_content)
        
        # 提取题目和选项
        question_info = self._extract_question(cleaned_content)
        
        return {
            "title": cleaned_title,
            "url": result.get("url", ""),
            "content": cleaned_content,
            "knowledge_points": knowledge_points,
            **question_info
        }
    
    def _clean_text(self, text):
        """
        清理文本
        
        Args:
            text: 原始文本
            
        Returns:
            清理后的文本
        """
        if not text:
            return ""
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 移除特殊字符
        text = re.sub(r'[\x00-\x1f\x7f-\xff]', '', text)
        
        return text.strip()
    
    def _extract_knowledge_points(self, text):
        """
        提取知识点
        
        Args:
            text: 文本内容
            
        Returns:
            知识点列表
        """
        knowledge_points = []
        
        # 常见知识点关键词
        keywords = [
            "动词辨析", "名词辨析", "形容词辨析", "副词辨析",
            "上下文语义", "固定搭配", "语法结构", "逻辑关系",
            "主旨大意", "细节理解", "推理判断", "词义猜测"
        ]
        
        for keyword in keywords:
            if keyword in text:
                knowledge_points.append(keyword)
        
        return list(set(knowledge_points))  # 去重
    
    def _extract_question(self, text):
        """
        提取题目和选项
        
        Args:
            text: 文本内容
            
        Returns:
            题目信息字典
        """
        question_info = {
            "question": "",
            "options": {},
            "answer": "",
            "analysis": ""
        }
        
        # 提取题目
        question_pattern = re.search(r'(\d+\s*[.\)]\s*.*?)(?=[A-D]\s*[.\)])', text, re.DOTALL)
        if question_pattern:
            question_info["question"] = question_pattern.group(1).strip()
        
        # 提取选项
        options_pattern = re.findall(r'[A-D]\s*[.\)]\s*(.*?)(?=[A-D]\s*[.\)]|答案|解析|$)', text, re.DOTALL)
        if options_pattern:
            for i, option in enumerate(options_pattern[:4]):  # 最多4个选项
                letter = chr(65 + i)  # A, B, C, D
                question_info["options"][letter] = option.strip()
        
        # 提取答案
        answer_pattern = re.search(r'答案[:：]\s*([A-D])', text)
        if answer_pattern:
            question_info["answer"] = answer_pattern.group(1)
        
        # 提取解析
        analysis_pattern = re.search(r'解析[:：]\s*(.*?)(?=\d+\s*[.\)]|答案|$)', text, re.DOTALL)
        if analysis_pattern:
            question_info["analysis"] = analysis_pattern.group(1).strip()
        
        return question_info
    
    def clean_results(self, results):
        """
        清理多个搜索结果
        
        Args:
            results: 搜索结果列表
            
        Returns:
            清理后的结果列表
        """
        cleaned_results = []
        for result in results:
            cleaned_result = self.clean_result(result)
            if cleaned_result.get("content"):
                cleaned_results.append(cleaned_result)
        return cleaned_results
