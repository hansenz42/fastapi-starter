# 设置环境变量
import sys
import os

# 增加 src 根目录
path = os.path.dirname(os.path.abspath(__file__)) + '/src'
sys.path.insert(0, path)

import run as run

if __name__ == '__main__':
    run.main()
