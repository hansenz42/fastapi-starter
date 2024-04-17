import yaml
from common.path import ROOT_DIR
from common.env import ENV
from common.util import deep_merge_dict
from typing import List, Dict

CONFIG_FOLDER = ROOT_DIR / 'res'
BASE_CONFIG_FILE = CONFIG_FOLDER / 'config.yml'


def get_key_in_config(root: Dict, key_list: List[str], ind: int):
    """
    递归搜索，检查字典路径是否存在
    """
    if ind >= len(key_list):
        raise KeyError(f"索引 {ind} 超出关键字列表长度")

    if key_list[ind] not in root:
        raise KeyError(f"关键字 {key_list[ind]} 不存在于配置文件中")

    elif isinstance(root[key_list[ind]], dict):
        if ind == len(key_list) - 1:
            # 关键字存在，且是字典，到达终止条件，终止并返回
            return root[key_list[ind]]
        # 关键字存在，且是字典，则继续递归
        return get_key_in_config(root[key_list[ind]], key_list, ind + 1)
    else:
        # 关键字存在，且不是字典，则返回值
        return root[key_list[ind]]


class ConfigManager:
    """
    配置文件管理器
    """
    def __init__(self):
        self.config_content = None
        self.config_path = None
        self.env = ENV
        self.load_file()

    def load_file(self):
        CONFIG_FILE_TEMPLATE = 'config_{}.yml'
        self.config_path = CONFIG_FOLDER / CONFIG_FILE_TEMPLATE.format(self.env)

        try:
            self.config_content = yaml.load(open(BASE_CONFIG_FILE, 'r'), Loader=yaml.FullLoader) # 读取基础配置文件
            patch_config = yaml.load(open(self.config_path, 'r'), Loader=yaml.FullLoader)
        except Exception as e:
            raise IOError(f"配置文件读取失败，路径: {self.config_path}")

        self.config_content = deep_merge_dict(self.config_content, patch_config)

    def get_value(self, *args, **kwargs) -> any:
        """
        获取配置文件中的值
        """
        if self.config_content is None:
            return IOError("配置文件未加载")

        # 将 args 转为 list[str]
        args_str = [str(arg) for arg in args]

        return get_key_in_config(self.config_content, args_str, 0)


config_manager: ConfigManager = ConfigManager()

__all__ = [config_manager]