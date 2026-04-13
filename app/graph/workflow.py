from app.graph.nodes import Nodes
from app.models.llm_api import LLMAPI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, StateGraph, START
from pydantic import BaseModel
from typing import List, Dict, Any

# 定义状态模型
class State(BaseModel):
    question: str
    history: List[Dict[str, str]] = []
    response: str = ""
    category: str = ""

class Workflow:
    def __init__(self):
        self.nodes = Nodes()
        self.llm_api = LLMAPI()
        # 创建内存记忆存储
        self.memory = InMemorySaver()
        # 定义状态结构
        self.graph = StateGraph(State)
        # 添加节点
        self.graph.add_node("classify", self._classify_node)
        self.graph.add_node("greeting", self._greeting_node)
        self.graph.add_node("search", self._search_node)
        # 添加边
        self.graph.add_edge(START, "classify")
        self.graph.add_conditional_edges(
            "classify",
            lambda state: state.category,
            {
                "greeting": "greeting",
                "search": "search",
                "nonsense": "greeting"
            }
        )
        self.graph.add_edge("greeting", END)
        self.graph.add_edge("search", END)
        # 编译图
        self.app = self.graph.compile(checkpointer=self.memory)
    
    def _classify_node(self, state):
        """分类用户问题节点"""
        question = state.question
        history = state.history
        
        # 先进行简单的关键词匹配作为备份
        greeting_keywords = ["你好", "hello", "hi", "嗨", "早上好", "上午好", "下午好", "晚上好", "晚安", "再见", "bye"]
        question_lower = question.lower()
        for keyword in greeting_keywords:
            if keyword.lower() in question_lower:
                return {"category": "greeting", "history": history}
        
        # 检查是否包含考研相关关键词（不区分大小写）
        exam_keywords = ["考研", "英语", "真题", "阅读", "写作", "词汇", "语法", "听力", "翻译", "完型", "模拟题", "复习", "备考", "考试", "成绩", "分数线"]
        question_lower = question.lower()
        for keyword in exam_keywords:
            if keyword.lower() in question_lower:
                return {"category": "search", "history": history}
        
        # 检查是否包含大量乱码（如"??????"）
        if question.count("?") >= 3:
            # 如果包含大量乱码，默认返回search类型
            return {"category": "search", "history": history}
        
        # 然后使用LLM进行更智能的分类
        try:
            prompt = f"""请判断以下用户问题的类型，只能返回以下选项之一：
                    1. greeting - 问候语，如"你好"、"hello"、"早上好"等
                    2. search - 需要搜索考研英语相关信息的问题，如"如何提高考研英语阅读能力？"、"2023年考研英语真题"等
                    3. nonsense - 不知所云的内容，如乱码、无意义的字符或句子

                    用户问题：{question}

                    请直接返回类型，不要输出其他内容。"""
            
            # 收集流式输出
            response = ""
            for chunk in self.llm_api.generate(prompt):
                response += chunk
            
            response = response.strip().lower()
            
            # 确保返回值是有效的类型
            if response in ["greeting", "search", "nonsense"]:
                return {"category": response, "history": history}
            else:
                # 默认返回search类型
                return {"category": "search", "history": history}
        except Exception as e:
            print(f"分类问题失败: {e}")
            # 失败时返回search类型
            return {"category": "search", "history": history}
    
    def _greeting_node(self, state):
        """问候语节点"""
        question = state.question
        history = state.history
        
        # 生成问候语响应
        # 包含历史记录，让AI能够记住之前的对话内容
        history_str = "\n".join([f"用户: {item['content']}" if item['role'] == 'user' else f"助手: {item['content']}" for item in history])
        prompt = f"请用友好、自然的语言回应用户的问题，并且记住之前的对话内容：\n\n历史对话：\n{history_str}\n\n用户当前问题：{question}"
        response = ""
        for chunk in self.llm_api.generate(prompt):
            response += chunk
        
        # 更新历史记录
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": response})
        
        return {"response": response, "history": history}
    
    def _search_node(self, state):
        """搜索节点"""
        question = state.question
        history = state.history
        
        # 运行正常工作流，传递历史记录
        workflow_state = self.run(question, history)
        content = workflow_state.get('content', {})
        response = content.get('explanation', '')
        
        # 更新历史记录
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": response})
        
        return {"response": response, "history": history}
    
    def run(self, question, history=None):
        """运行工作流"""
        # 初始化状态
        state = {
            "question": question,
            "history": history or []
        }
        
        # 提取关键词
        state.update(self.nodes.extract_keywords(state))
        
        # 爬取试题
        state.update(self.nodes.crawl_questions(state))
        
        # 选择试题
        state.update(self.nodes.select_question(state))
        
        # 生成内容
        state.update(self.nodes.generate_content(state))
        
        return state
    
    def process_question(self, question, conversation_id="default"):
        """智能处理用户问题，判断是直接回答还是搜索"""
        try:
            # 尝试使用LangGraph运行工作流，获取响应
            result = self.app.invoke(
                {"question": question}, 
                config={"configurable": {"thread_id": conversation_id}}
            )
            
            # 检查result的类型，确保正确访问属性
            if hasattr(result, 'response'):
                response = result.response
            else:
                response = result.get("response", "")
            
            # 检查result中是否包含category字段
            if hasattr(result, 'category'):
                category = result.category
            else:
                category = result.get("category", "search")
            
            # 根据category字段的值判断是返回search类型的响应还是direct类型的响应
            if category == "search":
                # 如果是搜索模式，返回search类型的响应
                return {
                    "type": "search",
                    "content": {
                        "explanation": response
                    }
                }
            else:
                # 如果不是搜索模式，返回direct类型的响应（chat模式）
                return {
                    "type": "direct",
                    "content": {
                        "explanation": response,
                        "original_question": question,
                        "mindmap_path": ""
                    }
                }
        except Exception as e:
            print(f"处理问题失败: {e}")
            import traceback
            traceback.print_exc()
            # 如果发生异常，返回direct类型的响应（chat模式）
            return {
                "type": "direct",
                "content": {
                    "explanation": "抱歉，发生了错误，请稍后重试。",
                    "original_question": question,
                    "mindmap_path": ""
                }
            }
    
    def _classify_question(self, question):
        """使用LLM分类用户问题"""
        # 先进行简单的关键词匹配作为备份
        greeting_keywords = ["你好", "hello", "hi", "嗨", "早上好", "上午好", "下午好", "晚上好", "晚安", "再见", "bye"]
        question_lower = question.lower()
        for keyword in greeting_keywords:
            if keyword.lower() in question_lower:
                return "greeting"
        
        # 然后使用LLM进行更智能的分类
        try:
            prompt = f"""请判断以下用户问题的类型，只能返回以下选项之一：
                    1. greeting - 问候语，如"你好"、"hello"、"早上好"等
                    2. search - 需要搜索考研英语相关信息的问题，如"如何提高考研英语阅读能力？"、"2023年考研英语真题"等
                    3. nonsense - 不知所云的内容，如乱码、无意义的字符或句子

                    用户问题：{question}

                    请直接返回类型，不要输出其他内容。"""
            
            # 收集流式输出
            response = ""
            for chunk in self.llm_api.generate(prompt):
                response += chunk
            
            response = response.strip().lower()
            
            # 确保返回值是有效的类型
            if response in ["greeting", "search", "nonsense"]:
                return response
            else:
                # 默认返回search类型
                return "search"
        except Exception as e:
            print(f"分类问题失败: {e}")
            # 失败时返回search类型
            return "search"
    
    def _generate_greeting_response(self, question, stream=False):
        """生成问候语响应"""
        prompt = f"请用友好、自然的语言回应用户的问候：{question}"
        if stream:
            return self.llm_api.generate(prompt, stream=stream)
        else:
            # 收集流式输出并返回字符串
            response = ""
            for chunk in self.llm_api.generate(prompt, stream=stream):
                response += chunk
            return response
