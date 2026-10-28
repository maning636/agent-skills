#!/usr/bin/env python3
"""
蝉镜数字人视频生成器
===================
通过蝉镜AI开放平台API, 输入文案即可生成数字人口播视频。

前置条件:
  1. 蝉镜账号 (chanjing.cc) + API密钥
  2. pip install requests

用法:
  python chanjing_video.py "世界杯4年1次，熬夜看球是成年人最后的浪漫"
  python chanjing_video.py --text "你的文案" --person "海城" --output "output.mp4"

凭证配置 (优先级):
  1. 环境变量: CHANJING_APP_ID / CHANJING_SECRET_KEY
  2. 配置文件: ~/.chanjing/config.json {"app_id":"...", "secret_key":"..."}
  3. 命令行: --app-id xxx --secret-key xxx
"""
import argparse, json, os, sys, time, requests

BASE_URL = "https://open-api.chanjing.cc"
DEFAULT_PERSON = "ce393722e3b245bfa53d73bcec847ee3"  # 海城 (温和青年男生)

def get_credentials(app_id=None, secret_key=None):
    """获取凭证: 参数 > 环境变量 > 配置文件"""
    if app_id and secret_key:
        return app_id, secret_key
    env_id = os.environ.get("CHANJING_APP_ID")
    env_key = os.environ.get("CHANJING_SECRET_KEY")
    if env_id and env_key:
        return env_id, env_key
    config_file = os.path.expanduser("~/.chanjing/config.json")
    if os.path.exists(config_file):
        with open(config_file) as f:
            cfg = json.load(f)
        return cfg["app_id"], cfg["secret_key"]
    raise RuntimeError("未找到蝉镜凭证。请设置环境变量或 ~/.chanjing/config.json")

def get_token(app_id, secret_key):
    """获取AccessToken (24h有效)"""
    resp = requests.post(f"{BASE_URL}/open/v1/access_token",
        json={"app_id": app_id, "secret_key": secret_key}, timeout=15)
    data = resp.json()
    if data["code"] != 0:
        raise RuntimeError(f"Token获取失败: {data.get('msg')}")
    return data["data"]["access_token"]

def list_persons(token, gender=None):
    """列出可用的公共数字人"""
    resp = requests.get(f"{BASE_URL}/open/v1/list_common_dp",
        params={"page": 1, "size": 50},
        headers={"access_token": token}, timeout=15)
    data = resp.json()
    if data["code"] != 0:
        raise RuntimeError(f"获取列表失败: {data.get('msg')}")
    persons = []
    for p in data["data"]["list"]:
        if gender and p.get("gender") != gender:
            continue
        fig_types = [f["type"] for f in p.get("figures", [])]
        persons.append({
            "id": p["id"], "name": p["name"],
            "gender": p.get("gender"), "audio_name": p.get("audio_name"),
            "audio_man": p.get("audio_man_id"), "figures": fig_types
        })
    return persons

def create_video(token, person_id, text, figure_type="whole_body", model=1, speed=1.0):
    """
    创建数字人视频合成任务

    Args:
        token: AccessToken
        person_id: 数字人形象ID
        text: 口播文案 (≤4000字)
        figure_type: 姿态 (whole_body/sit_body/circle_view)
        model: 0=基础版 1=高质版 2=卡通专用
        speed: 语速 0.5~2.0

    Returns:
        video_id (str)
    """
    person_data = requests.get(f"{BASE_URL}/open/v1/list_common_dp",
        params={"page": 1, "size": 100},
        headers={"access_token": token}, timeout=15).json()

    audio_man = None
    person_name = "未知"
    for p in person_data.get("data", {}).get("list", []):
        if p["id"] == person_id:
            audio_man = p["audio_man_id"]
            person_name = p["name"]
            break
    if not audio_man:
        raise RuntimeError(f"数字人ID不存在: {person_id}")

    payload = {
        "person": {"id": person_id, "x": 0, "y": 480, "width": 1080, "height": 1440, "figure_type": figure_type},
        "audio": {"tts": {"text": [text], "speed": speed, "audio_man": audio_man}, "type": "tts", "volume": 100, "language": "cn"},
        "screen_width": 1080, "screen_height": 1920, "model": model
    }

    resp = requests.post(f"{BASE_URL}/open/v1/create_video",
        json=payload, headers={"access_token": token}, timeout=30)
    data = resp.json()
    if data["code"] != 0:
        raise RuntimeError(f"创建失败: {data.get('msg')}")
    video_id = data["data"]
    est_sec = len(text) * 234 / 1000
    print(f"✅ 任务已提交 | ID={video_id} | 数字人={person_name} | 预估{est_sec:.0f}秒")
    return video_id

def poll_and_download(token, video_id, output="output.mp4", max_wait=300):
    """轮询视频状态并下载"""
    for i in range(max_wait // 5):
        time.sleep(5)
        resp = requests.get(f"{BASE_URL}/open/v1/video",
            params={"id": video_id}, headers={"access_token": token}, timeout=15)
        data = resp.json()
        if data["code"] != 0:
            continue
        d = data["data"]
        status = d["status"]
        progress = d.get("progress", 0)

        if status == 30:
            vurl = d["video_url"]
            dl = requests.get(vurl, timeout=120)
            with open(output, "wb") as f:
                f.write(dl.content)
            print(f"✅ 下载完成 | {output} | {len(dl.content)/1024:.0f}KB | {d.get('duration', '?')}秒")
            return output
        elif status >= 40:
            raise RuntimeError(f"生成失败: status={status} msg={d.get('msg')}")
        else:
            print(f"  [{i+1}] 生成中... {progress}%")
    raise TimeoutError("视频生成超时")

def main():
    parser = argparse.ArgumentParser(description="蝉镜数字人视频生成器")
    parser.add_argument("text", nargs="?", help="口播文案")
    parser.add_argument("--text", "-t", dest="text_opt", help="口播文案")
    parser.add_argument("--person", "-p", default=DEFAULT_PERSON, help="数字人形象ID")
    parser.add_argument("--output", "-o", default="chanjing_output.mp4", help="输出文件")
    parser.add_argument("--speed", "-s", type=float, default=1.0, help="语速 (0.5-2.0)")
    parser.add_argument("--list", "-l", action="store_true", help="列出可用数字人")
    parser.add_argument("--figure", default="whole_body", choices=["whole_body","sit_body","circle_view"])
    parser.add_argument("--app-id", help="蝉镜 App ID")
    parser.add_argument("--secret-key", help="蝉镜 Secret Key")
    args = parser.parse_args()

    text = args.text or args.text_opt
    app_id, secret_key = get_credentials(args.app_id, args.secret_key)
    token = get_token(app_id, secret_key)

    if args.list:
        persons = list_persons(token)
        print(f"\n共 {len(persons)} 个可用的公共数字人:\n")
        for p in persons:
            print(f"  {p['id']} | {p['name']} | {p['gender']} | {p['audio_name']} | {p['figures']}")
        return

    if not text:
        print("请提供口播文案: python chanjing_video.py \"你的文案\"")
        sys.exit(1)

    print(f"文案: {text}")
    print(f"字数: {len(text)} | 预估时长: {len(text)*234/1000:.0f}秒")
    print(f"数字人: {args.person}\n")

    video_id = create_video(token, args.person, text, args.figure, speed=args.speed)
    poll_and_download(token, video_id, args.output)

if __name__ == "__main__":
    main()
