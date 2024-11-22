from main import Repo2LLM
from github_handler import GitHubHandler
from markdown_converter import MarkdownConverter

def process_repo(repo_url: str) -> str:
    repo2llm = Repo2LLM()
    github_handler = GitHubHandler()
    markdown_converter = MarkdownConverter()
    
    repo_contents = github_handler.get_repo_contents(repo_url)
    processed_files = []
    
    for item in repo_contents:
        try:
            if item['type'] == 'file' and not repo2llm.should_exclude(item['path']):
                content = github_handler.get_file_content(item['download_url'])
                processed_files.append({
                    'path': item['path'],
                    'content': content
                })
        except Exception as e:
            print(f"处理文件 {item['path']} 时出错: {str(e)}")
            continue
    
    return markdown_converter.convert_to_markdown(processed_files) 