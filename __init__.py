import random
from nonebot.plugin.on import on_message
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
)
from pathlib import Path
from typing import Union
try:
    import ujson as json
except ModuleNotFoundError:
    import json

DATA_PATH = Path()/ "data"
anime_data = json.load(open(DATA_PATH / "data.json", "r", encoding="utf8"))
ai=on_message(rule=to_me(), priority=99,block=False)

def get_message_text(data: Union[str, Message]) -> str:
    """
    说明：
        获取消息中 纯文本 的信息
    参数：
        :param data: event.json()
    """
    result = ""
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "text":
                result += msg["data"]["text"].strip() + " "
        return result.strip()
    else:
        for seg in data["text"]:
            result += seg.data["text"] + " "
    return result


def hello() -> str:
    """
    一些打招呼的内容
    """
    result = random.choice(
        (
            "哦豁？！",
            "你好！Ov<",
            f"库库库，呼唤{NICKNAME}做什么呢",
            "我在呢！",
            "呼呼，叫俺干嘛",
        )
    )
    return result

async def get_chat_result(text: str, user_id: int, nickname: str) -> str:
    if len(text) < 6:
        keys = anime_data.keys()
        for key in keys:
            if text.find(key) != -1:
                return random.choice(anime_data[key]).replace("你", nickname)


@ai.handle()
async def _(bot:Bot,event:MessageEvent):
    msg = get_message_text(event.json())
    if "CQ:xml" in str(event.get_message()):
        return
    # 打招呼
    if (not msg) or msg in [
        "你好啊",
        "你好",
        "在吗",
        "在不在",
        "您好",
        "您好啊",
        "你好",
        "在",
    ]:
        await ai.finish(hello())
    if isinstance(event, GroupMessageEvent):
        nickname = event.sender.card or event.sender.nickname
    else:
        nickname = event.sender.nickname
    result = await get_chat_result(msg, event.user_id, nickname)
    if result==None:
        return
    await ai.finish(Message(result))
