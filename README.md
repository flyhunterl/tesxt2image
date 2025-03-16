# Text2Image Plugin for DOW

一个用于将长文本自动转换为图片的DOW插件。当回复的文本超过设定字数时，插件会自动将文本转换为精美的图片进行发送，避免刷屏或者被折叠.提升用户阅读体验。

## 功能特点

- 自动检测回复的文本长度
- 超过设定字数时自动转换为图片
- 支持自定义背景图片
- 可配置的文本样式和图片参数
- 优雅的排版和展示效果

## 安装方法

1. 将插件文件夹复制到DOW的plugins目录下：


2. 扫描并启用插件

## 配置说明

在插件目录下的`config.json`文件中进行配置：

```json
{
    "imgrender_token": "Imgrender的密钥",
    "background_url": "图片链接",
    "image_height": 1600,
    "min_text_length": 200
}
```

配置项说明：
- `imgrender_token`: imgrender API的访问令牌（必填）
- `background_url`: 背景图片URL（可选）
- `image_height`: 生成图片的高度（默认1600）
- `min_text_length`: 触发转换的最小文本长度（默认200）

## 获取imgrender Token

1. 访问 [imgrender官网](https://www.imgrender.net/)
2. 注册并登录账号
3. 在控制台获取API Token
4. 将获取到的Token填入配置文件

## 背景图片资源

您可以在以下位置找到合适的背景图片：
- [堆糖-阅读背景专辑](https://www.duitang.com/album/?id=101698609&spm=2014.12553688.202.0)
- 推荐使用简洁的大理石纹理或浅色系背景图
- 推荐将图片上传到稳定的图床系统

## 使用示例

插件会自动工作，无需手动触发。当回复的文本超过配置的最小长度时，会自动将文本转换为图片发送。

## 常见问题

1. 图片生成失败
   - 检查imgrender_token是否正确
   - 确认API访问限额是否超限
   - 验证网络连接是否正常

2. 背景图显示异常
   - 确保background_url可以正常访问
   - 检查图片格式是否支持
   - 建议使用jpg/png格式的图片

## 技术支持

- 作者博客：[https://llingfei.com](https://llingfei.com)
- 问题反馈：请在GitHub提交Issue


## 打赏
**您的打赏能让我在下一顿的泡面里加上一根火腿肠。**
![20250314_125818_133_copy](https://github.com/user-attachments/assets/33df0129-c322-4b14-8c41-9dc78618e220)