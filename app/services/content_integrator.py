from app.models.llm_api import LLMAPI
from app.services.knowledge_extractor import KnowledgeExtractor
from app.services.mindmap_generator import MindmapGenerator

class ContentIntegrator:
    def __init__(self):
        self.llm_api = LLMAPI()
        self.knowledge_extractor = KnowledgeExtractor()
        self.mindmap_generator = MindmapGenerator()
    
    def integrate_content(self, question, analysis):
        """整合内容"""
        # 生成解释
        explanation = ""
        for chunk in self.llm_api.generate_explanation(question, analysis):
            explanation += chunk
        
        # 提取知识点
        knowledge_result = self.knowledge_extractor.extract_knowledge(question, analysis)
        knowledge_points = knowledge_result["knowledge_points"]
        
        # 生成思维导图
        mindmap_result = self.mindmap_generator.generate_mindmap(knowledge_points)
        mindmap_path = mindmap_result["mindmap_path"]
        
        return {
            "explanation": explanation,
            "original_question": question,
            "mindmap_path": mindmap_path
        }
    
    def generate_direct_answer(self, question, history=None):
        """直接生成回答"""
        # 构建历史记录字符串
        history_str = ""
        if history:
            history_str = "\n\n历史对话：\n"
            for item in history:
                if item['role'] == 'user':
                    history_str += f"用户: {item['content']}\n"
                else:
                    history_str += f"助手: {item['content']}\n"
        
        # 检查是否是询问原题的问题
        if any(keyword in question for keyword in ["原题", "题目", "原文", "完整题目", "完整原文"]):
            # 直接使用大模型生成原题
            prompt = f"请直接输出与以下查询相关的考研英语原题（包括完整题目、选项和原文）：{question}{history_str}\n\n要求：\n1. 直接输出原题，不要有任何多余的解释或引言\n2. 确保题目和选项完整\n3. 确保原文完整\n4. 按照考试年份、题型、文本类型等分类清晰输出"
            explanation = ""
            for chunk in self.llm_api.generate(prompt):
                explanation += chunk
        else:
            # 生成详细回答
            prompt = f"请详细回答以下考研英语相关问题：{question}{history_str}\n\n要求：\n1. 提供详细、准确的回答\n2. 包含相关知识点的讲解\n3. 语言清晰易懂，适合考研学生理解\n4. 可以提供一些学习建议或技巧\n5. 记住之前的对话内容，根据历史对话提供连贯的回答"
            explanation = ""
            for chunk in self.llm_api.generate(prompt):
                explanation += chunk
        
        return {
            "explanation": explanation,
            "original_question": "",
            "mindmap_path": ""
        }
