import json
import os
import requests
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
import plugins
from plugins import Plugin, Event, EventAction

@plugins.register(
    name="Text2Image",
    desire_priority=60,
    hidden=False,
    desc="将长文本转换为图片发送",
    version="0.1",
    author="Trae AI",
)
class Text2Image(Plugin):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.handlers[Event.ON_DECORATE_REPLY] = self.on_decorate_reply
        logger.info("[Text2Image] 插件已加载。")
        self.priority = 60

    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"[Text2Image] 加载配置文件失败: {e}")
            return {
                "imgrender_token": "",
                "background_url": "",
                "image_height": 800,
                "min_text_length": 100
            }

    def on_decorate_reply(self, e_context):
        """处理回复内容"""
        if e_context['reply'].type != ReplyType.TEXT:
            return

        content = e_context['reply'].content
        if not content or not isinstance(content, str):
            return

        # 检查文本长度是否超过设定值
        if len(content) < self.config.get("min_text_length", 100):
            return

        logger.info(f"[Text2Image] 检测到长文本回复，长度为 {len(content)}，准备转换为图片")
        
        try:
            # 调用 imgrender 服务将文本转换为图片
            image_url = self.text_to_image(content)
            if not image_url:
                logger.error("[Text2Image] 图片生成失败")
                return
            
            # 创建图片URL回复
            reply = Reply(ReplyType.IMAGE_URL)
            reply.content = image_url
            e_context['reply'] = reply
            e_context.action = EventAction.BREAK_PASS
            logger.info("[Text2Image] 已将文本回复转换为图片")
        except Exception as e:
            logger.error(f"[Text2Image] 处理回复时出错: {e}")

    def text_to_image(self, text):
        """将文本转换为图片，返回图片URL"""
        try:
            token = self.config.get("imgrender_token", "")
            if not token:
                logger.error("[Text2Image] imgrender_token 未设置")
                return None
                
            background_url = self.config.get("background_url", "")
            image_height = self.config.get("image_height", 800)
            
            # 使用正确的 API 端点和认证方式
            api_url = "https://api.imgrender.cn/open/v1/pics"
            
            # 调整为Apilot.py中使用的格式
            payload = {
                "width": 800,
                "height": image_height,
                "backgroundColor": "#f5f5f5",
                "images": [
                    {
                        "x": 0,
                        "y": 0,
                        "width": 800,
                        "height": image_height,
                        "url": background_url,
                        "zIndex": 0,
                        "opacity": 0.7
                    }
                ],
                "texts": [
                    {
                        "x": 70,
                        "y": 80,
                        "text": text,
                        "font": "SourceHanSansSC-Regular",
                        "fontSize": 32,
                        "color": "#333333",
                        "width": 660,
                        "textAlign": "left",
                        "lineHeight": 48,
                        "zIndex": 1
                    }
                ]
            }
            
            headers = {
                "X-API-Key": token,
                "Content-Type": "application/json; charset=utf-8"
            }
            
            response = requests.post(api_url, json=payload, headers=headers)
            logger.debug(f"[Text2Image] imgrender API响应: {response.text[:200]}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    # 直接返回图片URL，不下载图片内容
                    return result["data"]["url"]
                else:
                    logger.error(f"[Text2Image] API调用失败: {result.get('message')}")
                    return None
            else:
                logger.error(f"[Text2Image] API调用失败: {response.status_code}, {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"[Text2Image] 生成图片时出错: {e}")
            return None
            
    def get_help_text(self, verbose=False, **kwargs):
        short_help_text = "将长文本回复转换为图片发送"
        
        if not verbose:
            return short_help_text
            
        help_text = "📝 Text2Image 插件\n"
        help_text += "功能：自动检测超过设定字数的ChatGPT回复，将其转换为图片发送\n"
        help_text += "配置：可在 config.json 中设置 imgrender_token、背景图片和触发字数\n"
        
        return help_text