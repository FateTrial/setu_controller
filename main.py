import asyncio
import os
import json
import aiohttp
import logging
from astrbot.api.all import AstrMessageEvent, CommandResult, Context, Image, Plain
import astrbot.api.event.filter as filter
from astrbot.api.star import register, Star

logger = logging.getLogger("astrbot")

@register("FateTrial_setucontrollaer", "FateTrial", "一个涩涩的插件", "1.0.0")
class SetuPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.cd = 10  # 默认冷却时间为 10 秒
        self.last_usage = {} # 存储每个用户上次使用指令的时间
        self.semaphore = asyncio.Semaphore(10)  # 限制并发请求数量为 10
        self.config = config
        self.r18 = config.get("r18", "")
        self.size = config.get("size", "")
        

    @filter.command("涩涩")
    async def sese(self, message: AstrMessageEvent, prompt: str = ""):
        '''随机涩图'''
        url = f"https://image.anosu.top/pixiv/direct?r18={self.r18}&keyword={prompt}&size={self.size}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"获取图片失败: {resp.status}")
                    data = await resp.read()
        except Exception as e:
            logger.error(f"从 {url} 获取图片失败: {e}。")
        # 保存图片到本地
        try:
            with open("sese.jpg", "wb") as f:
                f.write(data)
            return CommandResult().file_image("sese.jpg")

        except Exception as e:
            return CommandResult().error(f"保存图片失败: {e}")

    @filter.command("sese_help")
    async def setu_help(self, event: AstrMessageEvent):
        help_text = """
        **涩涩插件帮助**

        **可用命令:**
        - `/sese`: 发送一张随机涩图。
        - `/sese_help`: 显示此帮助信息。

        **使用方法:**
        - 直接发送 `/sese` 即可获取一张随机涩图。
        - 涩图模式有青少年模式，青壮年模式和混合模式

        **注意:**
        - 涩图图片大小默认为 origin。
        """
        yield event.plain_result(help_text)