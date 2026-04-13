import os
from app.services.content_integrator import ContentIntegrator
from app.tools.utils.text_processor import TextProcessor
from app.tools.search.search_engine import SearchEngine
from app.tools.search.cleaner import ResultCleaner

class Nodes:
    def __init__(self):
        self.content_integrator = ContentIntegrator()
        self.text_processor = TextProcessor()
        self.search_engine = SearchEngine()
        self.result_cleaner = ResultCleaner()
    
    def extract_keywords(self, state):
        """提取关键词"""
        question = state.get("question", "")
        # 提取关键词
        keywords = self.text_processor.extract_keywords(question)
        return {"keywords": keywords}
    
    def crawl_questions(self, state):
        """使用Tavily搜索试题"""
        question = state.get("question", "")
        keywords = state.get("keywords", [])
        
        # 构建搜索查询
        search_query = question
        if keywords:
            search_query = f"{question} {' '.join(keywords)}"
        
        # 搜索试题
        results = self.search_engine.search_kaoyan_english(search_query)
        
        # 清理搜索结果
        cleaned_results = self.result_cleaner.clean_results(results)
        
        # 转换为标准格式
        questions = []
        for i, result in enumerate(cleaned_results):
            question_content = result.get("question", result.get("content", ""))
            options = result.get("options", {})
            
            # 构建试题内容
            formatted_question = question_content
            if options:
                formatted_question += "\n\n"
                for letter, option in options.items():
                    formatted_question += f"{letter}. {option}\n"
            
            questions.append({
                "title": result.get("title", f"搜索结果 {i+1}"),
                "url": result.get("url", ""),
                "content": {
                    "question": formatted_question.strip(),
                    "analysis": result.get("analysis", "")
                }
            })
        
        print(f"搜索到 {len(questions)} 道相关试题")
        return {"questions": questions}
    
    def select_question(self, state):
        """选择试题"""
        questions = state.get("questions", [])
        # 选择第一个试题
        selected_question = questions[0] if questions else None
        return {"selected_question": selected_question}
    
    def generate_content(self, state):
        """生成内容"""
        selected_question = state.get("selected_question", None)
        question = state.get("question", "")
        history = state.get("history", [])
        
        if not selected_question:
            # 当没有找到相关试题时，直接使用大模型生成回答
            content = self.content_integrator.generate_direct_answer(question, history)
            return {"content": content}
        
        # 提取试题和解析
        question = selected_question["content"]["question"]
        analysis = selected_question["content"]["analysis"]
        
        # 整合内容
        content = self.content_integrator.integrate_content(question, analysis)
        return {"content": content}
