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
        # 获取请求中的模式，如果没有则使用配置文件中的默认值
        mode = request.json.get('mode', None)
        logger.info(f"处理仓库: {repo_url}, 模式: {mode or '默认'}")
        
        # 初始化组件
        repo2llm = Repo2LLM()
        # 使用配置初始化 GitHubHandler，如果有指定模式则使用指定的
        github_handler = GitHubHandler(
            token=None,
            mode=mode or repo2llm.github_handler_config['mode'],
            shallow_clone=repo2llm.github_handler_config['shallow_clone']
        )
        markdown_converter = MarkdownConverter()
        logger.info("组件初始化完成")
        
        def generate():
            try:
                # 获取仓库内容
                logger.info("开始获取仓库内容")
                repo_contents = github_handler.get_repo_contents(repo_url)
                
                # 过滤文件
                logger.info("开始过滤需要处理的文件")
                valid_files = [
                    item for item in repo_contents 
                    if item['type'] == 'file' and not repo2llm.should_exclude(item['path'])
                ]
                total_files = len(valid_files)
                logger.info(f"找到 {total_files} 个需要处理的文件")
                
                # 开始处理的消息
                yield json.dumps({"type": "start", "total": total_files}) + '\n'
                
                processed_files = []
                processed_count = 0
                
                # 处理文件
                for item in valid_files:
                    try:
                        processed_count += 1
                        if 'content' in item:
                            # 克隆模式下，内容已经在item中
                            content = item['content']
                        else:
                            # HTTP模式下，需要通过download_url获取内容
                            content = github_handler.get_file_content(item['download_url'])
                            
                        processed_files.append({
                            'path': item['path'],
                            'content': content
                        })
                        
                        yield json.dumps({
                            "type": "progress",
                            "file": item['path'],
                            "current": processed_count,
                            "total": total_files
                        }) + '\n'
                        
                    except Exception as e:
                        logger.error(f"处理文件 {item['path']} 时出错: {str(e)}")
                        yield json.dumps({
                            "type": "error",
                            "file": item['path'],
                            "error": str(e)
                        }) + '\n'
                
                # 生成最终的 Markdown
                logger.info("生成 Markdown 输出...")
                markdown_output = markdown_converter.convert_to_markdown(processed_files)
                
                # 生成文件名
                owner_repo = repo_url.rstrip('/').split('/')[-2:]
                filename = f"{owner_repo[0]}_{owner_repo[1]}.md"
                output_path = OUTPUT_DIR / filename
                
                # 保存文件
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_output)
                
                # 完成消息
                yield json.dumps({
                    "type": "complete",
                    "filename": filename,
                    "content": markdown_output,
                    "total_processed": processed_count,
                    "total": total_files
                }) + '\n'
                
            except Exception as e:
                logger.error(f"处理过程中出错: {str(e)}")
                yield json.dumps({
                    "type": "error",
                    "error": str(e)
                }) + '\n'
        
        return Response(generate(), mimetype='text/event-stream')
        
    except Exception as e:
        logger.error(f"处理仓库时出错: {str(e)}")
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