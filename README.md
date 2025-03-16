# Text2Image 插件



一个用于将ChatGPT长文本回复转换为图片的插件，支持简单的Markdown格式渲染。

## 功能特点

- 自动检测超过设定字数的文本回复，将其转换为图片发送
- 支持简单的Markdown格式解析，包括标题、粗体、斜体、代码块、列表等
- 根据文本长度自动计算图片高度，或使用固定高度
- 支持自定义背景图片
- 完全使用API生成图片，不依赖本地图像处理库

## 安装方法

1. 将插件目录放置在 `plugins` 目录下
2. 安装依赖：`pip install requests`
3. 在 `config.json` 中配置imgrender API token和其他参数
4. 重启应用

## 配置参数

在 `config.json` 中可以设置以下参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| imgrender_token | 字符串 | "" | imgrender API的访问令牌（必填） |
| background_url | 字符串 | "" | 背景图片URL（可选） |
| min_text_length | 整数 | 100 | 触发转图片的最小文本长度 |
| enable_markdown_format | 布尔值 | true | 是否启用Markdown格式转换 |
| auto_height | 布尔值 | true | 是否启用自动高度计算 |
| fixed_height | 整数 | 800 | 固定高度模式下的图片高度（像素） |
| min_height | 整数 | 400 | 自动计算时的最小高度（像素） |
| max_height | 整数 | 2480 | 自动计算时的最大高度（像素） |
| height_per_100_chars | 整数 | 400 | 每100字符对应的高度（像素） |

## 配置示例

```json
{
    "imgrender_token": "your_token_here",
    "background_url": "https://example.com/background.jpg",
    "min_text_length": 200,
    "enable_markdown_format": true,
    "auto_height": true,
    "fixed_height": 1600,
    "min_height": 400,
    "max_height": 2480,
    "height_per_100_chars": 400
}
```

## Markdown支持

插件将Markdown格式转换为特定的纯文本格式进行渲染，支持以下Markdown元素：

- 标题（#、##、###）：转换为【标题内容】格式
- 粗体（**文本**）：转换为「文本」
- 斜体（*文本*）：转换为『文本』
- 代码块（```代码```）：添加缩进并用【代码】标记
- 行内代码（`代码`）：转换为『代码』
- 无序列表（- 或 *）：转换为• 符号
- 有序列表（1. 2.等）：保持原有格式
- 分隔线（---）：转换为横线

## 自动高度计算

当启用自动高度计算时（auto_height = true），插件会根据以下公式计算图片高度：

1. 基础高度 = 字符数 / 100 * height_per_100_chars
2. 额外高度 = 换行数 * 20
3. 总高度 = 基础高度 + 额外高度 + 160（顶部和底部边距）
4. 最终高度 = max(min_height, min(总高度, max_height))

这样可以确保图片高度与文本长度成正比，避免内容过多导致的溢出或空白过多。

## 注意事项

- imgrender API的最大图片高度限制为2480像素
- 需要有效的imgrender API token才能使用本插件
- 建议使用分辨率适中的背景图片，避免文件过大
- 如果文本包含大量的换行，可能需要调整height_per_100_chars参数

## 许可证

MIT License

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