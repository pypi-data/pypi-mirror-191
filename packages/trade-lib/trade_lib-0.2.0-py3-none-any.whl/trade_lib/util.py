import asyncio
import logging
import logging.config
import os
from functools import lru_cache
from pathlib import Path

import yaml
from yaml import Loader, load

logger = logging.getLogger(__name__)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def read_config(config_file):
    logger.info(f"config file: {config_file}")
    if os.path.isfile(config_file) and os.access(config_file, os.R_OK):
        with open(config_file, 'r') as f:
            return load(f, Loader=Loader)
    else:
        logger.error(f"{config_file} 文件不存在或不可读")
        exit(1)


def logging_config(config_file='logging.yml'):
    with open(config_file, 'r') as f_conf:
        dict_conf = yaml.safe_load(f_conf)
    logging.config.dictConfig(dict_conf)


def user_home_path():
    return Path.home()


def config_dir_path(dir='.config'):
    """
    返回用户当前目录下的配置目录
    :param dir:
    :return:
    """
    return os.path.join(Path.home(), dir)


@lru_cache
def read_yaml(yaml_file):
    if os.path.isfile(yaml_file) and os.access(yaml_file, os.R_OK):
        with open(yaml_file, 'r') as f:
            return load(f, Loader=Loader)
    else:
        raise Exception(f"{yaml_file} 文件不存在或不可读")


def get_exchange_config(name, file='exchanges.yaml'):
    """
    返回交易所用于 ccxt 的 api 配置
    :param name:
    :param cfg_file:
    :return:
    """
    try:
        path = config_dir_path()
        configs = read_yaml(path + '/' + file)
        return configs[name]
    except Exception as e:
        raise Exception(f"~/.config/{file} 中找不到 {name} 的 api 配置！")


async def repeat(interval, func, *args, **kwargs):
    """Run func every interval seconds.

    If func has not finished before *interval*, will run again
    immediately when the previous iteration finished.

    *args and **kwargs are passed as the arguments to func.
    """
    while True:
        try:
            await asyncio.gather(
                func(*args, **kwargs),
                asyncio.sleep(interval),
            )
        except asyncio.CancelledError:
            # logger.debug('repeat 退出')
            return
        except Exception as e:
            logger.exception('repeat')
            return


def dict_gets(d, keys, default=None):
    for key in keys:
        d = d.get(key, default)
        if isinstance(d, dict):
            continue
        else:
            return d
