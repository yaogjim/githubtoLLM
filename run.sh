#!/bin/bash

# 激活虚拟环境
# source venv/bin/activate

# 设置 PYTHONPATH
# export PYTHONPATH=$PYTHONPATH:$(pwd)/src

# 设置 Flask 环境变量（可选）
export FLASK_ENV=development
export FLASK_DEBUG=1

# 启动应用
python src/repo2llm/app.py which