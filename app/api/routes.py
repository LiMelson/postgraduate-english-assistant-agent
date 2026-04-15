from flask import Blueprint, request, jsonify, Response
import time
import os
from app.graph.workflow import Workflow

api_bp = Blueprint('api', __name__)
workflow = Workflow()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "service": "考研英语辅助Agent",
        "version": "1.0.0",
        "timestamp": time.time()
    })

@api_bp.route('/ask', methods=['POST'])
def ask_question():
    """处理用户问题"""
    try:
        # 获取请求数据
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({"message": "请输入问题"}), 400
        
        # 运行工作流
        result = workflow.run(question)
        
        # 获取内容
        content = result.get('content', {})
        
        return jsonify(content)
    except Exception as e:
        print(f"处理请求失败: {e}")
        return jsonify({"message": "处理请求失败，请稍后重试"}), 500

@api_bp.route('/process', methods=['POST'])
def process_question():
    """处理用户问题，智能判断是直接回答还是搜索（流式输出）"""
    try:
        # 获取请求数据
        data = request.json
        question = data.get('question', '')
        conversation_id = data.get('conversation_id', 'default')
        
        if not question:
            return jsonify({"message": "请输入问题"}), 400
        
        # 运行工作流，传递会话ID
        result = workflow.process_question(question, conversation_id)
        
        def generate():
            # 开始流式输出
            yield '{"type": "' + result['type'] + '", "content": {"explanation": "'
            
            # 逐字输出响应
            explanation = result['content'].get('explanation', '')
            for char in explanation:
                # 对特殊字符进行转义，确保JSON格式正确
                char = char.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
                yield char
                time.sleep(0.01)  # 控制输出速度
            
            # 结束流式输出
            yield '"}}'
        
        return Response(generate(), mimetype='application/json')
    except Exception as e:
        print(f"处理请求失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"message": "处理请求失败，请稍后重试", "error": str(e)}), 500
