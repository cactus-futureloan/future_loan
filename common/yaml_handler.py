import yaml


def read_yaml(file):
    """读取yaml文件"""
    with open(file, "r", encoding="utf-8") as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
        return conf


def write_yaml(file, data):
    """yaml文件写入内容"""
    with open(file, "w", encoding="utf-8") as f:
        yaml.dump(f, data)


if __name__ == '__main__':
    conf = read_yaml("E:\Auto_test\config\config.yml")
    print(conf)