import os
import json
from app.models.llm_api import LLMAPI
from config.settings import MINDMAP_CONFIG

class MindmapGenerator:
    def __init__(self):
        self.llm_api = LLMAPI()
        self.output_dir = MINDMAP_CONFIG["output_dir"]
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_mindmap(self, knowledge_points):
        """生成思维导图"""
        # 生成思维导图JSON
        mindmap_json = self.llm_api.generate_mindmap(knowledge_points)
        
        # 保存思维导图
        mindmap_path = self._save_mindmap(mindmap_json)
        
        return {
            "mindmap_json": mindmap_json,
            "mindmap_path": mindmap_path
        }
    
    def _save_mindmap(self, mindmap_json):
        """保存思维导图"""
        # 生成文件名
        import time
        timestamp = int(time.time())
        filename = f"mindmap_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # 保存文件
        try:
            # 尝试解析JSON，确保格式正确
            mindmap_data = json.loads(mindmap_json)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(mindmap_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存思维导图失败: {e}")
            # 如果JSON解析失败，直接保存原始文本
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(mindmap_json)
        
        return filepath
