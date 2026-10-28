#!/usr/bin/env python3
"""
小红书封面生成器
================
从wallpapercave下载高清壁纸, 生成1080x1440竖屏封面。

用法:
  python xhs_cover.py --title "C罗不在场" --subtitle "葡萄牙反而赢了" --color C8102E
  python xhs_cover.py --wp-id wp14175359 --title "深夜看球" --subtitle "一个人的世界杯"

依赖:
  pip install Pillow
"""
import argparse, os, urllib.request
from PIL import Image, ImageDraw, ImageFont

DESKTOP = os.path.expanduser("~/Desktop")
FONT_PATH = r"C:\Windows\Fonts\msyhbd.ttc"

def download_wp(wp_id):
    """从wallpapercave下载壁纸"""
    url = f"https://wallpapercave.com/wp/{wp_id}.jpg"
    src = os.path.join(DESKTOP, f"_src_{wp_id}.jpg")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = r.read()
    if len(data) < 50000:
        raise ValueError(f"图片太小: {len(data)} bytes")
    with open(src, "wb") as f:
        f.write(data)
    return src

def make_cover(src_path, out_path, title, subtitle, color="C8102E",
               title_size=54, subtitle_size=90, top_y=48, bot_y=1285):
    """
    生成1080x1440竖屏封面

    Args:
        src_path: 源图路径
        out_path: 输出路径
        title: 顶部小标题
        subtitle: 底部大标题
        color: 文字颜色(不带#) 如 'C8102E' '2E7D32' '1F4E79'
    """
    img = Image.open(src_path).convert("RGB")
    W, H = img.size
    TW, TH = 1080, 1440

    # 居中裁切
    crop_w = int(H * TW / TH)
    crop_w = min(crop_w, W)
    left = (W - crop_w) // 2
    img = img.crop((left, 0, left + crop_w, H))
    img = img.resize((TW, TH), Image.LANCZOS)

    # 上下暗条
    top_overlay = Image.new("RGBA", (TW, 130), (0, 0, 0, 160))
    bot_overlay = Image.new("RGBA", (TW, 230), (0, 0, 0, 170))
    img = img.convert("RGBA")
    img.paste(top_overlay, (0, 0), top_overlay)
    img.paste(bot_overlay, (0, 1210), bot_overlay)

    draw = ImageDraw.Draw(img)
    ft = ImageFont.truetype(FONT_PATH, title_size)
    fb = ImageFont.truetype(FONT_PATH, subtitle_size)

    # 4方向描边
    for dx, dy in [(-3,-3),(3,-3),(-3,3),(3,3)]:
        draw.text((540+dx, top_y+dy), title, font=ft, fill="#000000")
    draw.text((540, top_y), title, font=ft, fill="#" + color)

    for dx, dy in [(-3,-3),(3,-3),(-3,3),(3,3)]:
        draw.text((540+dx, bot_y+dy), subtitle, font=fb, fill="#000000")
    draw.text((540, bot_y), subtitle, font=fb, fill="#" + color)

    img.convert("RGB").save(out_path, quality=95)
    print(f"✅ {out_path} ({os.path.getsize(out_path)/1024:.0f}KB)")
    return out_path

def test_wp_ids(wp_ids):
    """批量测试壁纸ID可用性"""
    print(f"测试 {len(wp_ids)} 个壁纸ID...\n")
    working = []
    for wp in wp_ids:
        url = f"https://wallpapercave.com/wp/{wp}.jpg"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                sz = len(r.read())
            ok = sz > 50000
            print(f"  {wp}: {'OK' if ok else 'SMALL'} ({sz/1024:.0f}KB)")
            if ok:
                working.append(wp)
        except Exception as e:
            print(f"  {wp}: FAIL ({str(e)[:40]})")
    print(f"\n可用: {len(working)}/{len(wp_ids)}")
    return working

def main():
    parser = argparse.ArgumentParser(description="小红书封面生成器")
    parser.add_argument("--title", "-t", required=True, help="顶部标题")
    parser.add_argument("--subtitle", "-s", required=True, help="底部副标题")
    parser.add_argument("--color", "-c", default="C8102E", help="文字颜色(不带#)")
    parser.add_argument("--wp-id", default="wp14175359", help="壁纸ID")
    parser.add_argument("--output", "-o", help="输出路径 (默认桌面)")
    parser.add_argument("--test", nargs="+", help="测试多个壁纸ID")
    args = parser.parse_args()

    if args.test:
        test_wp_ids(args.test)
        return

    src = download_wp(args.wp_id)
    out = args.output or os.path.join(DESKTOP, f"cover_{args.wp_id}.png")
    make_cover(src, out, args.title, args.subtitle, args.color)
    os.remove(src)  # 清理临时文件

if __name__ == "__main__":
    main()
