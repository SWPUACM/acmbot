from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
from .commands import *

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-swpuacm",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)
