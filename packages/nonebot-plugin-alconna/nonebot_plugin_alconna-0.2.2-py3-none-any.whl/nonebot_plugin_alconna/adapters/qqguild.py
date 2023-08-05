from nonebot_plugin_alconna.typings import gen_unit
from nonebot_plugin_alconna.analyser import MessageContainer
from nepattern import (
    BasePattern,
    PatternModel,
    UnionArg,
)
from nepattern.main import INTEGER, URL

MessageContainer.config(
    preprocessors={
        "MessageSegment": lambda x: str(x) if x.type == "text" else None,
        "Text": lambda x: str(x)
    }
)

Text = str
Ark = gen_unit("ark")
Embed = gen_unit("embed")
Emoji = gen_unit("emoji")
Image = gen_unit("attachment")
FileImage = gen_unit("file_image")
MentionUser = gen_unit("mention_user")
MentionChannel = gen_unit("mention_channel")

ImgOrUrl = (
    UnionArg(
        [
            BasePattern(
                model=PatternModel.TYPE_CONVERT,
                origin=str,
                converter=lambda _, x: x.data['url'],
                alias="img",
                accepts=[Image],
            ),
            URL,
        ]
    )
    @ "img_url"
)
"""
内置类型, 允许传入图片元素(Image)或者链接(URL)，返回链接
"""

MentionID = (
    UnionArg(
        [
            BasePattern(
                model=PatternModel.TYPE_CONVERT,
                origin=int,
                alias="MentionUser",
                accepts=[MentionUser],
                converter=lambda _, x: int(x.data["user_id"]),
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
    @ "mention_id"
)
"""
内置类型，允许传入提醒元素(Mention)或者'@xxxx'式样的字符串或者数字, 返回数字
"""
