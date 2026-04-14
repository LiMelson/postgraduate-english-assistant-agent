import openai
from config.settings import LLM_CONFIG
from datetime import datetime

now=datetime.now()
class LLMAPI:
    def __init__(self):
        self.api_key = LLM_CONFIG["api_key"]
        self.model = "deepseek-chat"
        self.temperature = LLM_CONFIG["temperature"]
        self.max_tokens = LLM_CONFIG["max_tokens"]
        self.api_base = LLM_CONFIG["api_base"]
        
        # 初始化客户端
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )

        # ✅ 在这里统一开启流式输出，后面所有方法都自动流式！
        self.stream = True

    def generate(self, prompt, stream=None):
        """生成文本（全局流式）"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"你是一位专业的考研英语辅导老师，擅长与学生交流并提供帮助。当前时间是{now.strftime('%Y-%m-%d %H:%M:%S')}。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=stream if stream is not None else self.stream  # 使用传入的stream参数或默认值
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            print(f"生成文本失败: {e}")
            yield "生成文本失败，请稍后重试。"

    def generate_explanation(self, question, analysis):
        """生成试题解释（全局流式）"""
        prompt = f"请详细解释以下考研英语试题，并基于提供的解析给出更深入的分析：\n\n试题：{question}\n\n解析：{analysis}\n\n要求：\n1. 解释试题的考察点\n2. 分析解题思路\n3. 提供相关知识点的扩展\n4. 语言清晰易懂，适合考研学生理解"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的考研英语辅导老师，擅长解析考研英语试题并提供详细的知识点讲解。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=self.stream
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            print(f"生成解释失败: {e}")
            yield "生成解释失败，请稍后重试。"

    def extract_knowledge_points(self, text):
        """提取知识点（全局流式）"""
        prompt = f"请从以下文本中提取考研英语相关的知识点，并按照层级结构组织：\n\n{text}\n\n要求：\n1. 提取核心知识点\n2. 按照层级结构组织，从宏观到微观\n3. 每个知识点简要说明其重要性\n4. 格式清晰，便于生成思维导图"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的考研英语辅导老师，擅长从试题和解析中提取核心知识点。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=self.stream
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            print(f"提取知识点失败: {e}")
            yield "提取知识点失败，请稍后重试。"

    def generate_mindmap(self, knowledge_points):
        """生成思维导图（全局流式）"""
        prompt = f"请根据以下知识点生成一个结构化的思维导图，使用JSON格式输出：\n\n{knowledge_points}\n\n要求：\n1. 使用JSON格式输出，包含节点和子节点\n2. 每个节点包含id、text和children字段\n3. 层级结构清晰，从宏观到微观\n4. 确保JSON格式正确"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的教育技术专家，擅长将知识点组织成结构化的思维导图。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=self.stream
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            print(f"生成思维导图失败: {e}")
            yield "生成思维导图失败，请稍后重试。"
