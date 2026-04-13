import re
import jieba
from config.settings import KNOWLEDGE_EXTRACTOR_CONFIG

class TextProcessor:
    def __init__(self):
        self.stop_words = self._load_stop_words()
    
    def _load_stop_words(self):
        """加载停用词"""
        stop_words = set()
        try:
            with open(KNOWLEDGE_EXTRACTOR_CONFIG["stop_words_file"], 'r', encoding='utf-8') as f:
                for line in f:
                    stop_words.add(line.strip())
        except Exception as e:
            print(f"加载停用词失败: {e}")
        return stop_words
    
    def clean_text(self, text):
        """清理文本"""
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符
        text = re.sub(r'[\r\n\t]', ' ', text)
        # 去除首尾空白
        text = text.strip()
        return text
    
    def extract_keywords(self, text):
        """提取关键词"""
        # 清理文本
        text = self.clean_text(text)
        # 分词
        words = jieba.cut(text)
        # 过滤停用词和短词
        keywords = []
        for word in words:
            if word not in self.stop_words and len(word) >= KNOWLEDGE_EXTRACTOR_CONFIG["min_keyword_length"]:
                keywords.append(word)
        # 限制关键词数量
        return keywords[:KNOWLEDGE_EXTRACTOR_CONFIG["max_keywords"]]
    
    def split_sentences(self, text):
        """分割句子"""
        # 清理文本
        text = self.clean_text(text)
        # 分割句子
        sentences = re.split(r'[。！？.!?]', text)
        # 过滤空句子
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def extract_entities(self, text):
        """提取实体"""
        # 清理文本
        text = self.clean_text(text)
        # 提取实体（简单实现，实际项目中可以使用更复杂的NLP工具）
        entities = []
        # 提取英文单词
        english_words = re.findall(r'[a-zA-Z]+', text)
        entities.extend(english_words)
        # 提取数字
        numbers = re.findall(r'\d+', text)
        entities.extend(numbers)
        return entities
