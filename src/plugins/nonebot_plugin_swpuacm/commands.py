from nonebot import on_command, on_notice
from nonebot.matcher import Matcher
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupIncreaseNoticeEvent
from nonebot.log import logger

from .constant import __version__, PY_VERSION

import nonebot

add_request = on_notice(priority=2, block=True)
help_command = on_command("help", priority=1, block=True)
bot_command = on_command("bot", priority=1, block=True)
q_a_command = on_command("qa", priority=1, block=True)


@add_request.handle()
async def handle_request(event: GroupIncreaseNoticeEvent, matcher: Matcher):
    logger.debug(f"收到群成员增加通知：{event.user_id}")
    return await matcher.finish(
        MessageSegment.at(event.user_id)
        + " 欢迎加入西南石油大学ACM团队招新群！\n"
        + "我是机器人天在水。你可以使用[.help]获取使用帮助，使用[.bot]获取机器人信息。\n"
        + "在开始之前，请先阅读我们的群公告。如果你有意加入我们并开始学习一些基础知识，你可以在群文件中找到相关资料。\n"
        + "Copyleft (c) 2006-2024 ACM-SWPU"
    )


@help_command.handle()
async def handle_help(event: Event, matcher: Matcher):
    return await matcher.finish(
        MessageSegment.at(event.get_user_id())
        + " 你好，我是天在水，欢迎查看使用帮助。\n"
        + "[.help] - 查看此帮助信息\n"
        + "[.bot] - 查看机器人信息\n"
        + "[.qa] - ACM团队相关问答\n"
        + "此节点未挂载智能体，如有疑问请联系管理员。"
    )


@bot_command.handle()
async def handle_bot(matcher: Matcher):
    return await matcher.finish(
        f"天在水 v{__version__} by ACM-SWPU [Python {PY_VERSION} For Nonebot {nonebot.__version__}]\n"
        + "“醉后不知天在水，慢船清梦压星河。”欢迎加入ACM招新群！我是天在水，使用[.help]获取使用帮助。"
    )


@q_a_command.handle()
async def handle_q_a(event: Event, matcher: Matcher):
    logger.debug(f"收到群聊问答：{event.get_message()}")
    return await matcher.finish(
        MessageSegment.at(event.get_user_id()) + " 请等待此功能开发中..."
    )
