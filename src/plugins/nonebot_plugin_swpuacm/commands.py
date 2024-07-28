from nonebot import on_command, on_notice, on_request
from nonebot.matcher import Matcher
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupIncreaseNoticeEvent
from nonebot.log import logger


add_request = on_notice(priority=2, block=True)
q_a_command = on_command("qa", priority=1, block=True)


@add_request.handle()
async def handle_request(event: GroupIncreaseNoticeEvent, matcher: Matcher):
    logger.info(f"收到群成员增加通知：{event.user_id}")
    return await matcher.finish(
        MessageSegment.at(event.user_id)
        + " 欢迎西南石油大学ACM团队招新群！\n"
        + "我是机器人天在水。在此之前，请先阅读我们的群公告。\n"
        + "如果你有意加入我们并开始学习一些基础知识，你可以在群文件中找到相关资料。\n"
        + "Copyleft (c) 2006-2022 ACM-SWPU"
    )


@q_a_command.handle()
async def handle_q_a(event: Event, matcher: Matcher):
    logger.info(f"收到群聊问答：{event.get_message()}")
    return await matcher.finish(
        MessageSegment.at(event.get_user_id()) + " 请等待此功能开发中..."
    )
