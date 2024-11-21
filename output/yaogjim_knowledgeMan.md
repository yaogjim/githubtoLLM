# Repository Contents

## File Structure

```
README.md
wwg_finder.py```

## File Contents

### README.md

```markdown
# knowledgeMan
```

### wwg_finder.py

```python
import os
import shutil
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_and_move_wwg_files(input_dir, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created output directory: {output_dir}")

    # 遍历input目录
    logging.info(f"Starting to search for WWG files in: {input_dir}")
    files_moved = 0
    for root, dirs, files in os.walk(input_dir):
        logging.debug(f"Searching in directory: {root}")
        for file in files:
            if file.lower().startswith('wwg'):  # 使用小写比较，以防文件名大小写不一致
                # 构建源文件路径和目标文件路径
                src_path = os.path.join(root, file)
                dst_path = os.path.join(output_dir, file)
                
                try:
                    # 移动文件
                    shutil.move(src_path, dst_path)
                    logging.info(f"Moved: {src_path} -> {dst_path}")
                    files_moved += 1
                except Exception as e:
                    logging.error(f"Error moving file {src_path}: {str(e)}")

    logging.info(f"Total files moved: {files_moved}")

if __name__ == "__main__":
    # 指定输入和输出目录
    input_directory = '/Volumes/workspace/linsten/pan/download/input/'
    output_directory = '/Volumes/workspace/linsten/pan/download/input_WWG/'

    logging.info("Starting WWG file moving process")
    logging.info(f"Input directory: {input_directory}")
    logging.info(f"Output directory: {output_directory}")

    # 调用函数
    find_and_move_wwg_files(input_directory, output_directory)
    logging.info("WWG file moving process completed.")
```

