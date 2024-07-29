from nonebot import on_command, on_notice
from nonebot.matcher import Matcher
from nonebot.adapters import Event
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupIncreaseNoticeEvent
from nonebot.log import logger

from .constant import __version__, PY_VERSION

import tomlkit as toml
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
    command = event.get_plaintext()[5:].strip()
    if not command:
        return await matcher.finish(
            MessageSegment.at(event.get_user_id())
            + " 你好，我是天在水，欢迎查看使用帮助。\n"
            + "[.help] - 查看此帮助信息\n"
            + "[.bot] - 查看机器人信息\n"
            + "[.qa] - ACM团队相关问答\n"
            + "使用[.help [命令]]获取指定命令的帮助信息。\n"
            + "此节点未挂载智能体，如有疑问请联系管理员。"
        )
    else:
        match command:
            case "bot":
                return await matcher.finish("bot - 展示机器人信息")
            case "qa":
                return await matcher.finish(
                    "qa [ID|QUESTION] - ACM团队相关问答\n"
                    + "- qa 展示Q&A列表\n"
                    + "- qa [ID] 展示 ID 对应的解答\n"
                    + "- qa ask [问题] 发起新的提问，提问将会被递交至ACM团队，"
                    + "新生队长"
                    + MessageSegment.at("2030549481")
                    + " "
                    + MessageSegment.at("1728395677")
                    + "将会为你们的问题作出解答，你也可以直接联系我们。"
                )
            case _:
                return await matcher.finish(
                    MessageSegment.at(event.get_user_id())
                    + " 未知命令，请使用[.help]查看帮助信息。"
                )


@bot_command.handle()
async def handle_bot(matcher: Matcher):
    return await matcher.finish(
        f"天在水 v{__version__} by ACM-SWPU [Python {PY_VERSION} For Nonebot {nonebot.__version__}]\n"
        + "“醉后不知天在水，慢船清梦压星河。”欢迎加入ACM招新群！我是天在水，使用[.help]获取使用帮助。"
    )


@q_a_command.handle()
async def handle_q_a(event: Event, matcher: Matcher, bot: Bot):
    coms = str(event.get_message()).split()
    
    with open("src/plugins/nonebot_plugin_swpuacm/res/QAList.toml", 'r') as QAListF:
        QAList = toml.load(QAListF)
        QAListK = QAList.keys()
    with open("src/plugins/nonebot_plugin_swpuacm/res/settings.toml", 'r') as setting:
        settings = toml.load(setting)
        old_group = settings["old_group"]
        new_group = settings["new_group"]
        admins = settings["administrators"]
        
    if len(coms) == 1:
        msg = MessageSegment.at(event.get_user_id()) + " 以下是Q&A列表："
        for no in QAListK:
            msg += f"\n{no}. {QAList[no]['Q']}" # type: ignore
        return await matcher.finish(msg)

    elif coms[1] in QAListK:
        if QAList[coms[1]]['A'] == "None": # type: ignore
            return await matcher.finish(
                MessageSegment.at(event.get_user_id())
                + " 对不起，这个问题还没有被解答，请耐心等待"
            )
        return await matcher.finish(
            MessageSegment.at(event.get_user_id())
            + f"\nQ: {QAList[coms[1]]['Q']}" # type: ignore
            + f"\nA: {QAList[coms[1]]['A']}" # type: ignore
        )

    elif coms[1] == "ask":
        try:
            ques = coms[2]
        except IndexError:
            return await matcher.finish(
                MessageSegment.at(event.get_user_id())
                + " 请在 .qa ask 指令后加上你想问的问题"
            )
        else:
            new_no = str(len(QAListK) + 1)
            QAList.add(new_no, {}) # type: ignore
            QAList[new_no].add('Q', ques) # type: ignore
            QAList[new_no].add('A', "None") # type: ignore
            with open("src/plugins/nonebot_plugin_swpuacm/res/QAList.toml", 'wt') as QAListF:
                toml.dump(QAList, QAListF)
            
            msg = "新的问题已经出现：\n" + ques + f"\n序号为{new_no}。请使用命令\n“.qa answer {new_no} [问题的答案]”\n对问题进行回答。"
            await bot.send_group_msg(group_id = old_group, message = msg)
            return await Matcher.finish(
                MessageSegment.at(event.get_user_id())
                + f" 问题已经追加到Q&A列表，序号为{new_no}。请耐心等待队长"
                + MessageSegment.at("2030549481")
                + " "
                + MessageSegment.at("1728395677")
                + " 解答。"
            )
            
    elif coms[1] == "answer":
        if int(event.get_user_id()) not in admins: # type: ignore
            return await matcher.finish(
                MessageSegment.at(event.get_user_id())
                + " 您的权限不足，无法将该回答添加到Q&A列表"
            )
        elif len(coms) == 2:
            return await matcher.finish(
                MessageSegment.at(event.get_user_id())
                + " 未给出问题的编号和答案。请重试。"
            )
        elif len(coms) == 3:
            try:
                ans_no = int(coms[2])
            except ValueError:
                return await matcher.finish(
                    MessageSegment.at(event.get_user_id())
                    + " 未指明问题的编号。请重试。"
                )
            else:
                if coms[2] not in QAListK:
                    return await matcher.finish(
                        MessageSegment.at(event.get_user_id())
                        + " 该编号不存在。请重试。"
                    )
                return await matcher.finish(
                    MessageSegment.at(event.get_user_id())
                    + " 未给出问题的答案。请重试。"
                )
        else:
            ans_no = coms[2]
            answer = coms[3]
            try:
                int(ans_no)
            except ValueError:
                return await matcher.finish(
                    MessageSegment.at(event.get_user_id())
                    + " 你似乎把编号和问题放反了。请重试。"
                )
            else:
                if coms[2] not in QAListK:
                    return await matcher.finish(
                        MessageSegment.at(event.get_user_id())
                        + " 该编号不存在。请重试。"
                    )
                else:  
                    QAList[ans_no]['A'] = answer # type: ignore
                    with open("src/plugins/nonebot_plugin_swpuacm/res/QAList.toml", 'wt') as QAListF:
                        toml.dump(QAList, QAListF)
                    msg = f"{ans_no}号问题已经被解答。请使用“.qa {ans_no}”获取回答。"
                    await bot.send_group_msg(group_id = new_group, message = msg)
                    return await matcher.finish(
                        MessageSegment.at(event.get_user_id())
                        + f" {ans_no}号问题的答案已收录进Q&A列表。"
                    )
                    
    else:
        return await matcher.finish(
            MessageSegment.at(event.get_user_id())
            + " 未知命令，请使用[.help]查看帮助信息。"
        )
