# 设置环境变量
import sys
import os
os.environ['PYTHON_SERVICE_ENV'] = 'test'

# 增加 src 根目录
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src'
sys.path.insert(0, path)