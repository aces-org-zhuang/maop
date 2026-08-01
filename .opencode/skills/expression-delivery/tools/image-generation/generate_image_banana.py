#!/usr/bin/env python3
"""
Gemini Banana Pro (Nano Banana) 图片生成脚本

用法:
    python generate_image_banana.py --prompt "提示词" [--aspect_ratio 16:9] [--resolution 2K] [--output output.png]
    python generate_image_banana.py -p "提示词" -r 2K -o output.png

环境变量:
    BANANA_API_KEY: Gemini Native API 密钥

首次使用:
    1. 设置环境变量: export BANANA_API_KEY="your-api-key"
    2. 或保存到 .env 文件: echo 'BANANA_API_KEY="your-api-key"' >> .env
    3. 或直接输入: 脚本会提示您输入 API Key

支持分辨率: 1K, 2K, 4K
支持宽高比: 21:9, 16:9, 4:3, 3:2, 1:1, 9:16, 3:4, 2:3, 5:4, 4:5

API Key 获取说明:
    访问 https://console.cloud.google.com/apis/credentials?project=_ 获取 Gemini API Key
"""

import argparse
import base64
import os
import sys
import requests
from datetime import datetime
from pathlib import Path


# 默认配置 - Gemini Native API
DEFAULT_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent"
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_RESOLUTION = "2K"
DEFAULT_OUTPUT_DIR = "assets"  # 默认输出目录（相对路径）

SUPPORTED_ASPECT_RATIOS = ["21:9", "16:9", "4:3", "3:2", "1:1", "9:16", "3:4", "2:3", "5:4", "4:5"]
SUPPORTED_RESOLUTIONS = ["1K", "2K", "4K"]

# 超时配置（秒）
TIMEOUT_MAP = {"1K": 180, "2K": 300, "4K": 360}

# API Key 获取说明
API_KEY_INSTRUCTIONS = """
============================================
  Gemini Banana Pro API Key 获取指南
============================================

需要 API Key 才能使用图片生成功能。

获取步骤:
1. 访问 Google Cloud Console:
   https://console.cloud.google.com/apis/credentials?project=_

2. 使用 Google 账号登录（如没有，需要注册，免费）

3. 点击 "Create Credentials" > "API Key"

4. 复制生成的 API Key

5. 选择以下方式之一配置:
   
   方式 A - 保存到 .env 文件:
     echo 'BANANA_API_KEY="您的API Key"' >> .env
   
   方式 B - 设置环境变量:
     export BANANA_API_KEY="您的API Key"
   
   方式 C - 直接在下方输入:
     输入您的 API Key 并按回车

注意:
- API Key 可以免费注册获取
- 有免费配额限制，请查看 Google Cloud 控制台
- 请妥善保管您的 API Key，不要泄露给他人
============================================
"""


def get_api_key_from_env():
    """从环境变量获取 API Key"""
    return os.environ.get("BANANA_API_KEY", "").strip()


def get_api_key_from_env_file(cwd=None):
    """从 .env 文件获取 API Key"""
    if cwd is None:
        cwd = Path.cwd()
    
    # 尝试多个可能的 .env 位置
    env_paths = [
        cwd / ".env",
        Path(__file__).parent.parent.parent / ".env",  # skill 根目录
        Path.home() / ".env",
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and line.startswith("BANANA_API_KEY="):
                        key, value = line.split("=", 1)
                        return value.strip().strip('"').strip("'")
    return ""


def request_api_key():
    """交互式请求用户输入 API Key"""
    print(API_KEY_INSTRUCTIONS)
    print("\n请输入您的 Banana API Key (输入后按回车): ", end="")
    
    try:
        api_key = input().strip()
        return api_key
    except (EOFError, KeyboardInterrupt):
        print("\n操作已取消。")
        return ""


def save_api_key_to_env_file(api_key, cwd=None):
    """保存 API Key 到 .env 文件"""
    if cwd is None:
        cwd = Path.cwd()
    
    env_path = cwd / ".env"
    
    lines = []
    if env_path.exists():
        with open(env_path, "r") as f:
            lines = f.readlines()
    
    # 检查是否已存在 BANANA_API_KEY
    found = False
    new_lines = []
    for line in lines:
        if line.strip().startswith("BANANA_API_KEY="):
            new_lines.append(f'BANANA_API_KEY="{api_key}"\n')
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        new_lines.append(f'BANANA_API_KEY="{api_key}"\n')
    
    with open(env_path, "w") as f:
        f.writelines(new_lines)
    
    return True


def get_api_key(interactive=True, cwd=None):
    """
    获取 API Key
    
    优先级:
    1. 环境变量 BANANA_API_KEY
    2. .env 文件
    3. 交互式输入（如果 interactive=True）
    """
    # 1. 尝试从环境变量获取
    api_key = get_api_key_from_env()
    if api_key:
        return api_key
    
    # 2. 尝试从 .env 文件获取
    api_key = get_api_key_from_env_file(cwd)
    if api_key:
        return api_key
    
    # 3. 交互式请求（仅在命令行模式）
    if interactive and sys.stdin.isatty():
        api_key = request_api_key()
        if api_key:
            # 自动保存到 .env 文件
            save_api_key_to_env_file(api_key, cwd)
            print(f"\n✓ API Key 已保存到 {cwd / '.env'}")
            return api_key
    
    return ""


def generate_image(prompt: str, aspect_ratio: str = DEFAULT_ASPECT_RATIO,
                  resolution: str = DEFAULT_RESOLUTION,
                  output_path: str = None, api_key: str = None,
                  cwd: str = None) -> dict:
    """
    使用 Gemini Native API 生成图片

    Args:
        prompt: 图片描述提示词
        aspect_ratio: 宽高比
        resolution: 分辨率 (1K, 2K, 4K)
        output_path: 输出文件路径
        api_key: API 密钥（如果为 None，自动从环境变量/.env/交互式获取）
        cwd: 当前工作目录（用于查找 .env 文件）

    Returns:
        dict: {"success": bool, "image_path": str or None, "error": str or None}
    """
    if not api_key:
        api_key = get_api_key(interactive=True, cwd=cwd)

    if not api_key:
        return {
            "success": False,
            "error": "BANANA_API_KEY not found. 请设置 BANANA_API_KEY 环境变量或创建 .env 文件。\n获取 API Key: https://console.cloud.google.com/apis/credentials?project=_",
            "image_path": None
        }

    if aspect_ratio not in SUPPORTED_ASPECT_RATIOS:
        return {
            "success": False,
            "error": f"Unsupported aspect_ratio: {aspect_ratio}. Supported: {SUPPORTED_ASPECT_RATIOS}",
            "image_path": None
        }

    if resolution not in SUPPORTED_RESOLUTIONS:
        return {
            "success": False,
            "error": f"Unsupported resolution: {resolution}. Supported: {SUPPORTED_RESOLUTIONS}",
            "image_path": None
        }

    # API Key 通过 URL 参数传递
    api_url = f"{DEFAULT_API_URL}?key={api_key}"

    headers = {"Content-Type": "application/json"}

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

    print(f"[Banana] Generating image...")
    print(f"[Banana] Aspect ratio: {aspect_ratio}")
    print(f"[Banana] Resolution: {resolution}")
    print(f"[Banana] Prompt length: {len(prompt)} chars")

    timeout = TIMEOUT_MAP.get(resolution, 300)

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()

        data = response.json()

        # 检查响应结构
        if "candidates" not in data or not data["candidates"]:
            return {"success": False, "error": f"No candidates: {data}", "image_path": None}

        candidate = data["candidates"][0]

        # 检查 finishReason
        finish_reason = candidate.get("finishReason", "")
        if finish_reason != "STOP":
            safety_ratings = candidate.get("safetyRatings", [])
            return {
                "success": False,
                "error": f"Generation rejected. finishReason: {finish_reason}, safetyRatings: {safety_ratings}",
                "image_path": None
            }

        # 提取图片数据
        try:
            image_base64 = candidate["content"]["parts"][0]["inlineData"]["data"]
        except (KeyError, TypeError) as e:
            return {"success": False, "error": f"Failed to extract image: {e}", "image_path": None}

        image_bytes = base64.b64decode(image_base64)

        # 生成输出文件名
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # 使用默认输出目录 assets
            output_path = f"{DEFAULT_OUTPUT_DIR}/banana_output_{timestamp}.png"

        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_path, "wb") as f:
            f.write(image_bytes)

        file_size = os.path.getsize(output_path) / 1024
        print(f"[Banana] Success! Image saved: {output_path} ({file_size:.1f} KB)")

        return {"success": True, "image_path": output_path, "error": None}

    except requests.exceptions.Timeout:
        return {"success": False, "error": f"Request timeout (>{timeout}s)", "image_path": None}
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
        return {"success": False, "error": error_msg, "image_path": None}
    except Exception as e:
        return {"success": False, "error": str(e), "image_path": None}


def main():
    parser = argparse.ArgumentParser(
        description="Gemini Banana Pro 图片生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate_image_banana.py -p "a cute cat" -r 2K -o output.png
  python generate_image_banana.py --prompt "a flowchart" --resolution 4K

首次使用:
  设置环境变量: export BANANA_API_KEY="your-key"
  或保存到 .env:  echo 'BANANA_API_KEY="your-key"' >> .env
  或直接运行，脚本会提示您输入 API Key
        """
    )
    parser.add_argument("--prompt", "-p", required=True, help="图片描述提示词")
    parser.add_argument("--aspect_ratio", "-a", default=DEFAULT_ASPECT_RATIO,
                       choices=SUPPORTED_ASPECT_RATIOS,
                       help=f"宽高比 (default: {DEFAULT_ASPECT_RATIO})")
    parser.add_argument("--resolution", "-r", default=DEFAULT_RESOLUTION,
                       choices=SUPPORTED_RESOLUTIONS,
                       help=f"分辨率 (default: {DEFAULT_RESOLUTION})")
    parser.add_argument("--output", "-o", default=None,
                       help="输出文件路径 (default: 自动生成)")

    args = parser.parse_args()

    # 获取当前工作目录用于 .env 查找
    cwd = Path.cwd()

    result = generate_image(
        prompt=args.prompt,
        aspect_ratio=args.aspect_ratio,
        resolution=args.resolution,
        output_path=args.output,
        cwd=cwd
    )

    if result["success"]:
        print(f"\nOutput: {result['image_path']}")
        sys.exit(0)
    else:
        print(f"\nError: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
