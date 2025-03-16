import json
import os
import requests
import re
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
import plugins
from plugins import Plugin, Event, EventAction

@plugins.register(
    name="Text2Image",
    desire_priority=60,
    hidden=False,
    desc="将长文本转换为图片发送，支持简单Markdown格式",
    version="0.3",
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
                "min_text_length": 100,
                "enable_markdown_format": True,
                "auto_height": True,  # 是否启用自动高度计算
                "fixed_height": 800,  # 固定高度模式下使用的高度
                "min_height": 400,  # 最小图片高度
                "max_height": 2480,  # 最大图片高度，imgrender限制最大为2480
                "height_per_100_chars": 400,  # 每100字符对应的高度
                "text_x": 70,  # 文字X轴坐标
                "text_y": 80,  # 文字Y轴坐标
                "text_width": 660,  # 文字宽度
                "font_name": "SourceHanSansSC-Regular",  # 字体名称
                "font_size": 32,  # 字体大小
                "font_color": "#333333",  # 字体颜色
                "line_height": 48  # 行高
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

    def calculate_image_height(self, text):
        """根据文本长度计算适当的图片高度"""
        # 基本高度计算：每100字符约400像素
        height_per_100_chars = self.config.get("height_per_100_chars", 400)
        min_height = self.config.get("min_height", 400)
        max_height = self.config.get("max_height", 2480)  # imgrender限制最大高度为2480
        
        # 计算文本中的换行数量，每个换行额外增加一些高度
        newline_count = text.count('\n')
        
        # 计算基础高度：字符数量 / 100 * 高度比例
        char_count = len(text)
        base_height = int(char_count / 100 * height_per_100_chars)
        
        # 为换行增加额外高度（每个换行增加20像素）
        extra_height = newline_count * 20
        
        # 计算总高度并限制在最小/最大值范围内
        total_height = base_height + extra_height
        
        # 添加顶部和底部边距
        total_height += 160
        
        # 确保高度在合理范围内
        total_height = max(min_height, total_height)
        total_height = min(max_height, total_height)
        
        logger.info(f"[Text2Image] 计算图片高度: 文本长度={char_count}, 换行数={newline_count}, 计算高度={total_height}")
        return total_height

    def format_markdown(self, text):
        """简单格式化Markdown文本，保留基本结构"""
        if not self.config.get("enable_markdown_format", True):
            return text
            
        try:
            # 格式化标题
            text = re.sub(r'^# (.*?)$', r'\n\n【\1】\n', text, flags=re.MULTILINE)
            text = re.sub(r'^## (.*?)$', r'\n\n【\1】\n', text, flags=re.MULTILINE) 
            text = re.sub(r'^### (.*?)$', r'\n\n【\1】\n', text, flags=re.MULTILINE)
            
            # 格式化粗体和斜体
            text = re.sub(r'\*\*(.*?)\*\*', r'「\1」', text)
            text = re.sub(r'\*(.*?)\*', r'『\1』', text)
            
            # 格式化代码块，添加缩进
            def format_code_block(match):
                code = match.group(1).strip()
                # 每行添加4个空格缩进
                indented_code = "\n    " + code.replace("\n", "\n    ")
                return f"\n【代码】{indented_code}\n"
                
            text = re.sub(r'```(?:.*?)\n(.*?)```', format_code_block, text, flags=re.DOTALL)
            
            # 格式化行内代码
            text = re.sub(r'`(.*?)`', r'『\1』', text)
            
            # 格式化列表
            text = re.sub(r'^- (.*?)$', r'• \1', text, flags=re.MULTILINE)
            text = re.sub(r'^\* (.*?)$', r'• \1', text, flags=re.MULTILINE)
            text = re.sub(r'^(\d+)\. (.*?)$', r'\1. \2', text, flags=re.MULTILINE)
            
            # 保留分隔线
            text = re.sub(r'^---+$', r'\n----------\n', text, flags=re.MULTILINE)
            
            logger.info("[Text2Image] Markdown简单格式化完成")
            return text.strip()
        except Exception as e:
            logger.error(f"[Text2Image] Markdown格式化失败: {e}")
            return text

    def text_to_image(self, text):
        """将文本转换为图片，返回图片URL"""
        try:
            token = self.config.get("imgrender_token", "")
            if not token:
                logger.error("[Text2Image] imgrender_token 未设置")
                return None
                
            background_url = self.config.get("background_url", "")
            
            # 处理Markdown格式（如果启用）
            if self.config.get("enable_markdown_format", True):
                formatted_text = self.format_markdown(text)
            else:
                formatted_text = text
            
            # 根据文本长度自动计算图片高度或使用固定高度
            if self.config.get("auto_height", True):
                image_height = self.calculate_image_height(formatted_text)
                logger.info(f"[Text2Image] 使用自动计算的高度: {image_height}像素")
            else:
                image_height = self.config.get("fixed_height", 800)
                logger.info(f"[Text2Image] 使用固定高度: {image_height}像素")
            
            # 使用正确的 API 端点和认证方式
            api_url = "https://api.imgrender.cn/open/v1/pics"
            
            # 从配置中获取文字坐标和字体设置
            text_x = self.config.get("text_x", 70)
            text_y = self.config.get("text_y", 80)
            text_width = self.config.get("text_width", 660)
            font_name = self.config.get("font_name", "SourceHanSansSC-Regular")
            font_size = self.config.get("font_size", 32)
            font_color = self.config.get("font_color", "#333333")
            line_height = self.config.get("line_height", 48)
        
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
                        "x": text_x,
                        "y": text_y,
                        "text": formatted_text,
                        "font": font_name,
                        "fontSize": font_size,
                        "color": font_color,
                        "width": text_width,
                        "textAlign": "left",
                        "lineHeight": line_height,
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
        short_help_text = "将长文本回复转换为图片发送，支持简单Markdown格式"
        
        if not verbose:
            return short_help_text
            
        help_text = "📝 Text2Image 插件\n"
        help_text += "功能：自动检测超过设定字数的ChatGPT回复，将其转换为图片发送\n"
        help_text += "特性：支持简单Markdown格式转换（标题、粗体、斜体、代码块、列表等）\n"
        help_text += "      根据文本长度自动调整图片高度\n"
        help_text += "配置：可在 config.json 中设置 imgrender_token、背景图片和触发字数\n"
        
        return help_text