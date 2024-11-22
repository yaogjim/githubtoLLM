import requests
from typing import Dict, List
import base64
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class GitHubHandler:
    def __init__(self, token: str = None):
        self.token = token
        self.headers = {'Authorization': f'token {token}'} if token else {}
        logger.info("GitHub处理器初始化完成" + (" (带token)" if token else ""))
    
    def get_repo_contents(self, repo_url: str) -> List[Dict]:
        """递归获取仓库内容"""
        logger.info(f"开始获取仓库内容: {repo_url}")
        parts = repo_url.rstrip('/').split('/')
        owner, repo = parts[-2], parts[-1]
        
        def get_contents(path=''):
            api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
            logger.debug(f"请求 API: {api_url}")
            try:
                response = requests.get(api_url, headers=self.headers)
                response.raise_for_status()
                contents = response.json()
                
                all_contents = []
                if isinstance(contents, list):
                    for item in contents:
                        if item['type'] == 'dir':
                            logger.debug(f"递归获取目录: {item['path']}")
                            all_contents.extend(get_contents(item['path']))
                        else:
                            all_contents.append(item)
                else:
                    all_contents.append(contents)
                    
                return all_contents
            except requests.exceptions.RequestException as e:
                logger.error(f"获取仓库内容失败: {str(e)}")
                raise
        
        return get_contents()
    
    def get_file_content(self, file_url: str) -> str:
        """获取文件内容"""
        response = requests.get(file_url, headers=self.headers)
        response.raise_for_status()
        
        # 检查内容类型
        if 'application/json' in response.headers.get('content-type', ''):
            content = response.json()['content']
            return base64.b64decode(content).decode('utf-8')
        else:
            # 直接返回文本内容
            return response.text 