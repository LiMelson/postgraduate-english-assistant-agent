// 流式API调用
import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const askQuestion = async (question, onData, abortSignal, conversationId = 'default') => {
  try {
    // 直接使用fetch发送请求，确保正确处理流式响应
    const response = await fetch('/api/process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question, conversation_id: conversationId }),
      signal: abortSignal,
    });

    if (!response.ok) {
      throw new Error('API request failed');
    }

    const reader = response.body.getReader();
    let result = '';
    let currentExplanation = '';
    let currentType = 'direct';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = new TextDecoder().decode(value);
      result += chunk;
      
      // 提取当前的type部分
      const typeStart = result.indexOf('"type": "');
      if (typeStart !== -1) {
        const typeContentStart = typeStart + '"type": "'.length;
        const typeContentEnd = result.indexOf('"', typeContentStart);
        if (typeContentEnd !== -1) {
          currentType = result.substring(typeContentStart, typeContentEnd);
        }
      }
      
      // 提取当前的explanation部分
      // 查找explanation字段的位置
      const explanationStart = result.indexOf('"explanation": "');
      if (explanationStart !== -1) {
        // 提取explanation的值
        const contentStart = explanationStart + '"explanation": "'.length;
        // 找到下一个"}的位置
        const contentEnd = result.indexOf('"}}', contentStart);
        
        if (contentEnd !== -1) {
          // JSON完整，解析整个结果
          try {
            const parsed = JSON.parse(result);
            if (onData && parsed.content && parsed.content.explanation) {
              onData(parsed.content, parsed.type);
            }
          } catch (e) {
            // JSON解析错误，继续读取
          }
        } else {
          // JSON不完整，提取已有的explanation内容
          const partialExplanation = result.substring(contentStart);
          // 移除可能的转义字符
          currentExplanation = partialExplanation.replace(/\\"/g, '"').replace(/\\n/g, '\n').replace(/\\r/g, '\r');
          if (onData && currentExplanation) {
            onData({ explanation: currentExplanation }, currentType);
          }
        }
      }
    }

    const finalResult = JSON.parse(result);
    return finalResult.content;
  } catch (error) {
    console.error('Error calling API:', error);
    // 只有当错误不是AbortError时，才调用回调函数，传递错误信息
    if (onData && error.name !== 'AbortError') {
      onData({ explanation: '抱歉，发生了错误，请稍后重试。' });
    }
    // 只有当错误不是AbortError时，才返回错误内容
    if (error.name !== 'AbortError') {
      return { explanation: '抱歉，发生了错误，请稍后重试。' };
    }
    // 当错误是AbortError时，返回undefined，这样前端就不会显示错误信息
    return undefined;
  }
};

export default api;
