# 处理环境变量

import sys
import os
import getopt

ENV = None

# 在此列表中加入添加你自己的环境变量
VALID_ENVS = ['dev', 'prod', 'test']


def is_valid_env_candidate_str(candidate: str):
    """
    检查环境变量候选字符串是否合法
    """
    if candidate in VALID_ENVS:
        return True
    return False


def use_os_env():
    global ENV
    os_env = os.environ.get('PYTHON_SERVICE_ENV')
    if is_valid_env_candidate_str(os_env):
        ENV = os_env
        print('系统环境变量设置成功: ' + ENV)


def use_arg_env():
    global ENV

    try:
        opts, args = getopt.getopt(sys.argv[1:], "e:", ["env="])
        for opt, arg in opts:
            if opt in ("-e", "--env"):
                if is_valid_env_candidate_str(arg):
                    ENV = arg
                    print('命令行参数设置成功: ' + ENV)
    except getopt.GetoptError:
        pass


def use_default_env():
    global ENV
    ENV = 'dev'
    print('未传递环境变量，使用默认环境变量 dev')


use_arg_env()

if ENV is None:
    use_os_env()

if ENV is None:
    use_default_env()


__all__ = [ENV]