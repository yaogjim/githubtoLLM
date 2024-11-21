from flask import Flask, render_template, request, send_file, jsonify, url_for, Response, send_from_directory
from main import Repo2LLM
from github_handler import GitHubHandler
from markdown_converter import MarkdownConverter
from pathlib import Path
import os
import json
import logging

# 初始化日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 获取当前文件所在目录
current_dir = Path(__file__).parent
templates_dir = current_dir / 'templates'
static_dir = current_dir / 'static'

# 初始化 Flask 应用
app = Flask(__name__,
    template_folder=str(templates_dir),
    static_folder=str(static_dir)
)

# 确保使用项目根目录下的 output 目录
BASE_DIR = Path(__file__).parent.parent.parent
# 确保使用绝对路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / 'output'

# 确保输出目录存在
OUTPUT_DIR.mkdir(exist_ok=True)

logger.info(f"输出目录设置为: {OUTPUT_DIR}")
OUTPUT_DIR.mkdir(exist_ok=True)

@app.route('/')
def index():
    print(f"Static folder: {app.static_folder}")
    print(f"Static URL path: {app.static_url_path}")
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        logger.info("开始处理新的仓库请求")
        repo_url = request.json['repo_url']
        logger.info(f"处理仓库: {repo_url}")
        
        # 初始化组件
        repo2llm = Repo2LLM()
        github_handler = GitHubHandler()
        markdown_converter = MarkdownConverter()
        logger.info("组件初始化完成")
        
        # 获取仓库内容
        logger.info("开始获取仓库内容")
        repo_contents = github_handler.get_repo_contents(repo_url)
        processed_files = []

        # 过滤文件
        logger.info("开始过滤需要处理的文件")
        valid_files = [
            item for item in repo_contents 
            if item['type'] == 'file' and not repo2llm.should_exclude(item['path'])
        ]
        total_files = len(valid_files)
        logger.info(f"找到 {total_files} 个需要处理的文件")
        processed_count = 0
        
        def generate():
            nonlocal processed_count
            try:
                # 开始处理的消息
                yield json.dumps({"type": "start", "total": total_files}) + '\n'
                
                # 只遍历已过滤的文件列表
                for item in valid_files:
                    try:
                        content = github_handler.get_file_content(item['download_url'])
                        processed_files.append({
                            'path': item['path'],
                            'content': content
                        })
                        processed_count += 1
                        print(f"Processing {item['path']} ({processed_count}/{total_files})")
                        # 进度消息
                        yield json.dumps({
                            "type": "progress",
                            "file": item['path'],
                            "current": processed_count,
                            "total": total_files
                        }) + '\n'
                    except Exception as e:
                        print(f"Error processing {item['path']}: {str(e)}")
                        yield json.dumps({
                            "type": "error",
                            "file": item['path'],
                            "error": str(e)
                        }) + '\n'
                
                # 生成最终的 Markdown
                print("Generating markdown output...")
                markdown_output = markdown_converter.convert_to_markdown(processed_files)
                owner_repo = repo_url.rstrip('/').split('/')[-2:]
                filename = f"{owner_repo[0]}_{owner_repo[1]}.md"
                output_path = OUTPUT_DIR / filename
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_output)
                
                print(f"Completed processing. Total files: {processed_count}")
                # 修改完成消息的发送方式
                response_data = {
                    "type": "complete",
                    "filename": filename,
                    "content": markdown_output,
                    "total_processed": processed_count,
                    "total": total_files
                }
                yield json.dumps(response_data, ensure_ascii=False).encode('utf-8') + b'\n'
                
            except Exception as e:
                print(f"Error in generate: {str(e)}")
                yield json.dumps({
                    "type": "error",
                    "error": str(e)
                }) + '\n'
            
        return Response(generate(), mimetype='text/event-stream')
        
    except Exception as e:
        print(f"Error processing repository: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/download/<filename>')
def download(filename):
    """处理文件下载请求"""
    logger.info(f"收到下载请求: {filename}")
    
    try:
        # 构建完整的文件路径
        file_path = OUTPUT_DIR / filename
        logger.debug(f"查找文件路径: {file_path}")
        
        # 检查文件是否存在
        if not file_path.exists():
            logger.error(f"文件不存在: {file_path}")
            return jsonify({'error': '文件不存在'}), 404
        
        logger.info(f"开始发送文件: {file_path}")
        
        # 发送文件
        response = send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/markdown'
        )
        
        # 添加必要的响应头
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        response.headers["Access-Control-Allow-Origin"] = "*"
        
        logger.info(f"文件发送成功: {filename}")
        return response
        
    except Exception as e:
        logger.exception(f"下载文件时出错: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 