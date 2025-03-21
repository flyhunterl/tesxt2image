# Text2Image 插件



一个用于将DOW长文本回复转换为图片的插件，支持简单的Markdown格式渲染。

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
| text_x | 整数 | 70 | 文字X轴坐标（像素） |
| text_y | 整数 | 80 | 文字Y轴坐标（像素） |
| text_width | 整数 | 660 | 文字区域宽度（像素） |
| font_name | 字符串 | "SourceHanSansSC-Regular" | 字体名称 |
| font_size | 整数 | 32 | 字体大小（像素） |
| font_color | 字符串 | "#333333" | 字体颜色（十六进制） |
| line_height | 整数 | 48 | 行高（像素） |
| whitelist_keywords | 列表 | [] | 白名单关键词列表 |
| blacklist_keywords | 列表 | [] | 黑名单关键词列表 |
| emoji_display_mode | 字符串 | "text" | 表情显示模式："native"(原生emoji)、"text"(保留文本格式)、"description"(转为文字描述) |

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
    "height_per_100_chars": 400,
    "text_x": 70,
    "text_y": 80,
    "text_width": 660,
    "font_name": "SourceHanSansSC-Regular",
    "font_size": 32,
    "font_color": "#333333",
    "line_height": 48,
    "whitelist_keywords": ["图片", "照片", "截图"],
    "blacklist_keywords": ["代码", "程序", "源码"],
    "emoji_display_mode": "text"
}
```

## 表情符号处理

插件支持三种不同的表情符号处理模式，通过 `emoji_display_mode` 配置项设置：

- `text`：保留微信表情文本形式，如 `[憨笑]`。这是默认模式，适用于字体不支持 emoji 的情况。
- ~~`native`：将微信表情文本转换为原生 emoji 表情符号。如果渲染字体支持 emoji，建议使用此模式。~~ imgrender暂不支持
- `description`：将微信表情文本转换为文字描述，如 `(憨笑)`。当字体不支持 emoji 且希望更简洁的显示方式时可选用。

由于 imgrender API 和某些字体对表情符号的支持有限，选择合适的模式可以避免表情符号显示为方框（□）。

## 关键词过滤功能

插件支持通过白名单和黑名单关键词来控制文本的处理方式：

- `whitelist_keywords`：白名单关键词列表，包含这些关键词的文本将始终转换为图片，不受字数限制
- `blacklist_keywords`：黑名单关键词列表，包含这些关键词的文本将始终保持文字输出，不转换为图片

处理优先级：
1. 如果文本包含黑名单关键词 → 保持文字输出
2. 如果文本包含白名单关键词 → 转换为图片
3. 如果文本既不在黑名单也不在白名单中 → 检查文本长度，超过设定值则转换为图片

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


## 支持的字体

插件支持多种字体，按类型分类如下：

### 1. 书法字体
- jiangxizhuokai（江西拙楷）
- slideyouran（演示悠然小楷）

### 2. 思源黑体系列
- SourceHanSansSC-Heavy（思源黑体-特粗）
- SourceHanSansSC-Bold（思源黑体-粗）
- SourceHanSansSC-Medium（思源黑体-中等）
- SourceHanSansSC-Regular（思源黑体-常规）
- SourceHanSansSC-Normal（思源黑体-标准）
- SourceHanSansSC-Light（思源黑体-细）
- SourceHanSansSC-ExtraLight（思源黑体-特细）

### 3. 思源宋体系列
- SourceHanSerifCN-Heavy（思源宋体-特粗）
- SourceHanSerifCN-Bold（思源宋体-粗）
- SourceHanSerifCN-SemiBold（思源宋体-半粗）
- SourceHanSerifCN-Medium（思源宋体-中等）
- SourceHanSerifCN-Regular（思源宋体-常规）
- SourceHanSerifCN-Light（思源宋体-细）
- SourceHanSerifCN-ExtraLight（思源宋体-特细）

### 4. 阿里巴巴普惠体系列
- Alibaba-PuHuiTi-Heavy（阿里巴巴普惠体-特粗）
- Alibaba-PuHuiTi-Bold（阿里巴巴普惠体-粗）
- Alibaba-PuHuiTi-Medium（阿里巴巴普惠体-中等）
- Alibaba-PuHuiTi-Regular（阿里巴巴普惠体-常规）
- Alibaba-PuHuiTi-Light（阿里巴巴普惠体-细）

## 打赏
**您的打赏能让我在下一顿的泡面里加上一根火腿肠。**
![20250314_125818_133_copy](https://github.com/user-attachments/assets/33df0129-c322-4b14-8c41-9dc78618e220)


