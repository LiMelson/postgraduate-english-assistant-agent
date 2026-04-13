from app.models.llm_api import LLMAPI
from app.tools.utils.text_processor import TextProcessor

class KnowledgeExtractor:
    def __init__(self):
        self.llm_api = LLMAPI()
        self.text_processor = TextProcessor()
    
    def extract_knowledge(self, question, analysis):
        """提取知识点"""
        # 合并试题和解析
        combined_text = f"试题：{question}\n\n解析：{analysis}"
        
        # 提取知识点
        knowledge_points = self.llm_api.extract_knowledge_points(combined_text)
        
        # 提取关键词
        keywords = self.text_processor.extract_keywords(combined_text)
        
        return {
            "knowledge_points": knowledge_points,
            "keywords": keywords
        }
