from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class MarkdownConverter:
    def __init__(self):
        pass
    
    def convert_to_markdown(self, files: List[Dict[str, str]]) -> str:
        """将文件列表转换为 Markdown 格式"""
        logger.info("开始转换文件为 Markdown 格式")
        logger.info(f"需要处理的文件数量: {len(files)}")
        
        markdown = "# Repository Contents\n\n"
        
        # 添加文件结构信息
        logger.debug("生成文件结构树")
        markdown += "## File Structure\n\n"
        markdown += "```\n"
        markdown += self._generate_file_tree(files)
        markdown += "```\n\n"
        
        logger.debug("开始处理每个文件的内容")
        markdown += "## File Contents\n\n"
        
        for file in files:
            file_path = file['path']
            logger.debug(f"处理文件: {file_path}")
            content = file['content']
            
            markdown += f"### {file_path}\n\n"
            markdown += "```" + self._get_language(file_path) + "\n"
            markdown += content + "\n"
            markdown += "```\n\n"
        
        logger.info("Markdown 转换完成")
        return markdown
    
    def _generate_file_tree(self, files: List[Dict[str, str]]) -> str:
        """生成文件树结构"""
        paths = [file['path'] for file in files]
        paths.sort()
        
        # 构建目录树
        tree = []
        current_dirs = []
        
        for path in paths:
            parts = path.split('/')
            
            # 处理目录结构
            for i, part in enumerate(parts[:-1]):
                # 计算当前层级的完整路径
                current_path = '/'.join(parts[:i+1])
                
                # 如果这个目录还没有被添加到树中
                if current_path not in current_dirs:
                    indent = '  ' * i
                    tree.append(f"{indent}{'└── ' if indent else ''}{part}/")
                    current_dirs.append(current_path)
            
            # 添加文件
            indent = '  ' * (len(parts) - 1)
            tree.append(f"{indent}{'└── ' if indent else ''}{parts[-1]}")
        
        return '\n'.join(tree)
    
    def _get_language(self, file_path: str) -> str:
        """根据文件扩展名获取语言标识"""
        ext = Path(file_path).suffix.lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.md': 'markdown',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.json': 'json',
        }
        return language_map.get(ext, '') 