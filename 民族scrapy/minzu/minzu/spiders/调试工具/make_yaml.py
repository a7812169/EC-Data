import os
import shutil
from minzu.minzu.settings  import YAML_FILE_DIR
def new_yaml(config_file_name):
    config_file = config_file_name + ".yaml"
    _YAML_FILE_DIR = os.sep.join(("..", YAML_FILE_DIR))
    files = os.listdir(_YAML_FILE_DIR)
    if config_file in files:
        print("%s已存在,重新取个名字吧" % config_file)
    else:
        shutil.copy(_YAML_FILE_DIR + "mum.yaml", _YAML_FILE_DIR + config_file)
        print("%s新建成功" % config_file)
if __name__ == '__main__':
    name = "广西自治区"
    new_yaml(name)
