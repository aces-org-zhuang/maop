# Gemini Banana Pro (Nano Banana) API 参考

## 概述

Gemini Banana Pro (gemini-3-pro-image-preview) 是 Google 最新的 AI 图片生成模型，基于 Gemini 3 Pro 构建。

### 核心特性

- **4K 高清支持**: 1K, 2K, 4K 分辨率
- **业界最佳文字渲染**: 多语言文字清晰可读
- **支持最多 14 张参考图**: 保持角色/品牌一致性
- **高级局部编辑**: 摄像机角度、焦点、色彩分级、场景照明

---

## API 端点

### 谷歌原生格式（推荐）

```
POST https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent
```

### OpenAI 兼容模式

```
POST https://api.apiyi.com/v1/chat/completions
```

---

## 提示词技巧 (Prompt Tips)

### 核心公式

**[主体 + 形容词] 正在做 [动作] 在 [位置/背景]。[构图/摄像机角度]。[光线/氛围]。[风格/媒介]。[具体约束/文字]。**

### 七大技巧

#### 1. 建立愿景：故事、主体和风格

prompt 中应包含：
- **Subject (主体)**: 谁或什么是图片内容？要具体
  - 例如: `a stoic robot barista with glowing blue optics`
- **Composition (构图)**: 镜头如何取景？
  - 例如: `extreme close-up`, `wide shot`, `low angle shot`
- **Action (动作)**: 正在发生什么？
  - 例如: `brewing a cup of coffee`, `casting a magical spell`
- **Location (位置)**: 场景在哪里？
  - 例如: `a futuristic cafe on Mars`, `a sun-drenched meadow at golden hour`
- **Style (风格)**: 整体美学是什么？
  - 例如: `3D animation`, `film noir`, `watercolor painting`, `photorealistic`

#### 2. 完善细节：摄像机、光线和格式

- **构图和宽高比**:
  - `A 9:16 vertical poster`
  - `A cinematic 21:9 wide shot`
- **摄像机和光线细节**:
  - `A low-angle shot with a shallow depth of field (f/1.8)`
  - `Golden hour backlighting creating long shadows`
  - `Cinematic color grading with muted teal tones`
- **文字集成**: `The headline 'URBAN EXPLORER' rendered in bold, white, sans-serif font at the top`
- **事实约束（用于图表）**: `A scientifically accurate cross-section diagram`

#### 3. 技术图表专用提示词结构

```
[图表类型], showing [主题描述], [设计风格], [配色方案],
with [布局描述], professional [应用场景] style, white background,
high detail, [分辨率修饰]
```

**示例**:
```
A flowchart showing the user authentication process, clean modern design,
blue and white color scheme, with arrows indicating flow direction,
professional business style, white background, high detail, 4K resolution
```

#### 4. 迭代优化

- 如果图片大部分正确，**请求具体修改**而不是重新生成
- 例如: `Change the man's tie to green` 而不是 `Generate a man with green tie`

#### 5. 添加真实感细节

- `visible skin pores`
- `slight motion blur`
- `dust particles in the air`
- `imperfections for authenticity`

#### 6. 多参考图融合

- 最多支持 14 张参考图
- 清晰定义每张图的角色:
  - `Use Image A for the character's pose`
  - `Image B for the art style`
  - `Image C for the background environment`

#### 7. 保持品牌一致性

- 使用相同的参考图和风格描述
- `consistent brand styling`
- `preserve natural lighting and texture`

---

## 请求格式

### 谷歌原生格式

```json
{
  "contents": [{
    "parts": [{"text": "图片描述提示词"}]
  }],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9",
      "imageSize": "2K"
    }
  }
}
```

### 参数说明

| 参数 | 可选值 | 说明 |
|------|--------|------|
| aspectRatio | 21:9, 16:9, 4:3, 3:2, 1:1, 9:16, 3:4, 2:3, 5:4, 4:5 | 宽高比 |
| imageSize | 1K, 2K, 4K | 输出分辨率 |

### 宽高比选择

| 比例 | 适用场景 |
|------|----------|
| 9:16 | 竖屏视频（抖音、快手、Stories） |
| 16:9 | 横屏视频（YouTube、B站、网站横幅） |
| 1:1 | 社交媒体（Instagram、朋友圈） |
| 4:3 | 传统照片比例 |
| 21:9 | ultra-wide 屏幕/电影比例 |

### 分辨率选择

| 分辨率 | 适用场景 | 超时 |
|--------|----------|------|
| 1K | 社交媒体/网页 | 180s |
| 2K | 高清显示/打印（推荐） | 300s |
| 4K | 专业设计/商业用途 | 360s |

---

## Python 调用示例

### 基础调用

```python
import requests
import base64
from datetime import datetime

API_KEY = "your-api-key"
API_URL = "https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent"

def generate_image(prompt: str, aspect_ratio: str = "16:9",
                  resolution: str = "2K", output_path: str = None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": resolution
            }
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=300)

    if response.status_code == 200:
        data = response.json()
        image_base64 = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
        return base64.b64decode(image_base64)
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
```

### 完整示例（保存文件）

```python
import requests
import base64
import os
from datetime import datetime

API_KEY = "your-api-key"
API_URL = "https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent"

TIMEOUT_MAP = {"1K": 180, "2K": 300, "4K": 360}

def generate_image(prompt: str, aspect_ratio: str = "16:9",
                  resolution: str = "2K", output_dir: str = "."):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": resolution
            }
        }
    }

    print(f"Generating image... (aspect_ratio={aspect_ratio}, resolution={resolution})")

    response = requests.post(
        API_URL, headers=headers, json=payload,
        timeout=TIMEOUT_MAP.get(resolution, 300)
    )

    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    data = response.json()
    image_base64 = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    image_bytes = base64.b64decode(image_base64)

    # 保存文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = "png"  # 或从响应中检测
    output_path = os.path.join(output_dir, f"banana_{timestamp}.{ext}")

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    print(f"Image saved: {output_path} ({len(image_bytes) / 1024:.1f} KB)")
    return output_path

# 使用示例
if __name__ == "__main__":
    prompt = "A flowchart showing user authentication process, clean modern design, blue and white color scheme"
    generate_image(prompt, aspect_ratio="16:9", resolution="2K")
```

---

## 错误处理

### 常见错误检查

1. **candidatesTokenCount = 0**: 内容审核拒绝
2. **finishReason != STOP**: 安全过滤拒绝
3. **API 返回文本**: 直接展示拒绝说明

### 错误处理示例

```python
def generate_image_safe(prompt: str, **kwargs):
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=300)
        data = response.json()

        # 检查是否被拒绝
        if "candidates" not in data or not data["candidates"]:
            return {"success": False, "error": "No candidates returned", "detail": data}

        candidate = data["candidates"][0]

        # 检查 finishReason
        if candidate.get("finishReason") != "STOP":
            return {"success": False, "error": "Generation rejected", "detail": candidate}

        # 提取图片
        image_base64 = candidate["content"]["parts"][0]["inlineData"]["data"]
        return {"success": True, "image_base64": image_base64}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

---

## 当前局限性

- **文字渲染**: 小字体、细节、拼写可能不完美
- **事实准确性**: 图表类可视化请验证事实
- **多语言**: 可能存在语法错误或文化细节缺失
- **复杂编辑**: 混合或光线变化可能产生伪影
- **角色一致性**: 跨编辑可能有所变化

---

## 价格参考

| 分辨率 | 价格（约） |
|--------|-----------|
| 1K-2K | $0.05/张 |
| 4K | $0.05/张 |
