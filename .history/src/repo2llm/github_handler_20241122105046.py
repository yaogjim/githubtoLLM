import requests
from typing import Dict, List, Literal
import base64
from pathlib import Path
import logging
import tempfile
import git
import os

logger = logging.getLogger(__name__)

class GitHubHandler:
    def __init__(self, token: str = None, mode: str = "http", shallow_clone: bool = True):
        self.token = token
        self.headers = {'Authorization': f'token {token}'} if token else {}
        self.mode = mode
        self.shallow_clone = shallow_clone
        logger.info(f"GitHub处理器初始化完成 (模式: {mode}, 浅克隆: {shallow_clone})" + (" (带token)" if token else ""))
    
    def get_repo_contents(self, repo_url: str) -> List[Dict]:
        """递归获取仓库内容"""
        logger.info(f"开始获取仓库内容: {repo_url}")
        
        # 根据模式选择不同的实现
        if self.mode == "clone":
            return self._get_repo_contents_clone(repo_url)
        else:
            return self._get_repo_contents_http(repo_url)
    
    def _get_repo_contents_http(self, repo_url: str) -> List[Dict]:
        """通过HTTP API获取仓库内容"""
        logger.info(f"开始获取仓库内容_get_repo_contents_http: {repo_url}")
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
    
    def _get_repo_contents_clone(self, repo_url: str) -> List[Dict]:
        """通过克隆方式获取仓库内容"""
        logger.info(f"开始克隆仓库_get_repo_contents_clone: {repo_url}")
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # 克隆仓库
                if self.token:
                    logger.info("使用认证令牌克隆仓库")
                    auth_url = repo_url.replace('https://', f'https://oauth2:{self.token}@')
                    logger.debug(f"克隆目标目录: {temp_dir}")
                    repo = git.Repo.clone_from(auth_url, temp_dir, depth=1)
                else:
                    logger.info("使用匿名方式克隆公开仓库")
                    logger.debug(f"克隆目标目录: {temp_dir}")
                    repo = git.Repo.clone_from(repo_url, temp_dir, depth=1)
                logger.info("仓库克隆完成")
                
                # 遍历文件
                all_contents = []
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, temp_dir)
                        
                        # 读取文件内容
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            all_contents.append({
                                'path': rel_path,
                                'type': 'file',
                                'content': content,
                                'download_url': None  # 本地文件没有下载URL
                            })
                        except Exception as e:
                            logger.warning(f"无法读取文件 {rel_path}: {str(e)}")
                            continue
                
                return all_contents
                
            except Exception as e:
                logger.error(f"克隆仓库失败: {str(e)}")
                raise
    
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