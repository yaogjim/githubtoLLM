from pathlib import Path
import yaml
from typing import List, Set
import fnmatch
import requests
import base64
import json

class Repo2LLM:
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.excluded_patterns = set(self.config.get('exclude_patterns', []))
        self.excluded_extensions = set(self.config.get('exclude_extensions', []))
        self.github_handler_config = self.config.get('github_handler', {
            'mode': 'http',
            'shallow_clone': True
        })
    
    def _load_config(self, config_path: str) -> dict:
        if not config_path:
            return self._get_default_config()
            
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _get_default_config(self) -> dict:
        """如果没有提供配置文件，尝试加载默认配置文件"""
        default_config_path = Path(__file__).parent.parent.parent / 'config' / 'default_config.yml'
        if default_config_path.exists():
            with open(default_config_path, 'r') as f:
                return yaml.safe_load(f)
            
        # 如果默认配置文件不存在，返回最基本的配置
        return {
            'exclude_patterns': ['**/__pycache__/**', '**/.git/**'],
            'exclude_extensions': ['.pyc', '.pyo', '.pyd'],
            'exclude_files': ['LICENSE']
        }
    
    def should_exclude(self, file_path: str) -> bool:
        # 检查完整文件名
        file_name = Path(file_path).name
        if file_name in ['poetry.lock', 'mock_data.txt', 'LICENSE', 'LICENSE.txt', 'LICENSE.md']:
            return True
        
        # 检查文件扩展名
        if Path(file_path).suffix in self.excluded_extensions:
            return True
        
        # 检查文件路径模式
        return any(fnmatch.fnmatch(file_path, pattern) for pattern in self.excluded_patterns) 