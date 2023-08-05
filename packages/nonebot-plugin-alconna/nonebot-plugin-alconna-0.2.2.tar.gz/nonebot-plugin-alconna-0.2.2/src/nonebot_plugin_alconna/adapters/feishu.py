from nonebot_plugin_alconna.typings import gen_unit
from nonebot_plugin_alconna.analyser import MessageContainer
from nepattern import (
    BasePattern,
    PatternModel,
    UnionArg,
)
from nepattern.main import INTEGER
MessageContainer.config(
    preprocessors={"MessageSegment": lambda x: str(x) if x.type == "text" else None}
)

Text = str
At = gen_unit("at")
Post = gen_unit("post")
Image = gen_unit("image")
Interactive = gen_unit("interactive")
ShareChat = gen_unit("share_chat")
ShareUser = gen_unit("share_user")
Audio = gen_unit("audio")
Media = gen_unit("media")
File = gen_unit("File")
Sticker = gen_unit("sticker")


AtID = (
    UnionArg(
        [
            BasePattern(
                model=PatternModel.TYPE_CONVERT,
                origin=int,
                alias="At",
                accepts=[At],
                converter=lambda _, x: int(x.data['user_id']),
            ),
            BasePattern(
                r"@(\d+)",
                model=PatternModel.REGEX_CONVERT,
                origin=int,
                alias="@xxx",
                accepts=[str],
            ),
            INTEGER,
        ]
    )
    @ "at_id"
)
"""
内置类型，允许传入提醒元素(At)或者'@xxxx'式样的字符串或者数字, 返回数字
"""
