import os

import ruamel.yaml as yaml

cdirname = os.path.dirname(__file__)


def read_conf(name, server_type=None):
    if cdirname in name:
        file = open(name, encoding='utf-8')
    else:
        file = open(os.path.join(cdirname, f'../{name}'), encoding='utf-8')
    conf = yaml.load(file, Loader=yaml.Loader)
    if server_type is None:
        return conf
    else:
        return conf[server_type]


def read_yml(path):
    conf = yaml.load(open(path))
    return conf


if __name__ == '__main__':
    config = read_conf('hbase')
    print([':'.join([x['host'], str(x['port'])]) for x in config])