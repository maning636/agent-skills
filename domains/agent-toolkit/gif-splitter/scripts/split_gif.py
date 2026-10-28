#!/usr/bin/env python3
"""
GIF动图切分工具

将超过指定帧数的GIF文件自动拆分成多个小文件。
适用于微信公众号等平台上传GIF时遇到"帧数超限"的问题。

使用方法:
    python3 split_gif.py "文件或文件夹路径" [选项]

示例:
    python3 split_gif.py "动图.gif"                    # 切分单个文件
    python3 split_gif.py ~/gifs/                       # 切分文件夹中所有GIF
    python3 split_gif.py "动图.gif" --max-frames 200   # 自定义最大帧数
    python3 split_gif.py "动图.gif" --info             # 仅查看信息
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("错误: 需要安装 Pillow 库")
    print("请运行: pip3 install Pillow")
    sys.exit(1)


def get_gif_info(filepath: str) -> dict:
    """获取GIF文件信息"""
    with Image.open(filepath) as img:
        frames = []
        durations = []
        try:
            while True:
                frames.append(img.copy())
                durations.append(img.info.get('duration', 100))
                img.seek(img.tell() + 1)
        except EOFError:
            pass

        size_mb = os.path.getsize(filepath) / (1024 * 1024)

        return {
            'filepath': filepath,
            'filename': os.path.basename(filepath),
            'frame_count': len(frames),
            'size_mb': size_mb,
            'width': frames[0].width if frames else 0,
            'height': frames[0].height if frames else 0,
            'frames': frames,
            'durations': durations
        }


def print_gif_info(info: dict, max_frames: int):
    """打印GIF信息"""
    print(f"\n文件: {info['filename']}")
    print(f"帧数: {info['frame_count']} 帧")
    print(f"大小: {info['size_mb']:.2f} MB")
    print(f"尺寸: {info['width']}x{info['height']}")

    if info['frame_count'] > max_frames:
        num_parts = (info['frame_count'] + max_frames - 1) // max_frames
        print(f"状态: 需要切分（超过 {max_frames} 帧，将分成 {num_parts} 个文件）")
    else:
        print(f"状态: 无需切分（未超过 {max_frames} 帧）")


def split_gif(info: dict, output_dir: str, max_frames: int) -> list:
    """
    切分GIF文件

    返回: 生成的文件路径列表
    """
    frames = info['frames']
    durations = info['durations']
    total_frames = info['frame_count']
    name_without_ext = os.path.splitext(info['filename'])[0]

    # 如果不需要切分
    if total_frames <= max_frames:
        print(f"\n{info['filename']}: {total_frames} 帧，无需切分")
        return []

    # 计算切分方案
    num_parts = (total_frames + max_frames - 1) // max_frames
    frames_per_part = (total_frames + num_parts - 1) // num_parts

    print(f"\n处理: {info['filename']} ({total_frames} 帧)")
    print(f"  将拆分为 {num_parts} 个文件，每个约 {frames_per_part} 帧")

    output_files = []

    for i in range(num_parts):
        start_idx = i * frames_per_part
        end_idx = min((i + 1) * frames_per_part, total_frames)
        part_frames = frames[start_idx:end_idx]
        part_durations = durations[start_idx:end_idx]

        output_filename = f"{name_without_ext}_第{i+1}部分.gif"
        output_path = os.path.join(output_dir, output_filename)

        # 保存GIF
        part_frames[0].save(
            output_path,
            save_all=True,
            append_images=part_frames[1:],
            duration=part_durations,
            loop=0,
            optimize=True
        )

        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  ✓ {output_filename}: {len(part_frames)} 帧, {size_mb:.2f} MB")
        output_files.append(output_path)

    return output_files


def process_path(path: str, output_dir: str, max_frames: int, info_only: bool) -> tuple:
    """
    处理文件或文件夹

    返回: (处理的文件数, 生成的文件数)
    """
    path = os.path.expanduser(path)

    if not os.path.exists(path):
        print(f"错误: 路径不存在 - {path}")
        return 0, 0

    # 收集所有GIF文件
    gif_files = []
    if os.path.isfile(path):
        if path.lower().endswith('.gif'):
            gif_files.append(path)
        else:
            print(f"错误: 不是GIF文件 - {path}")
            return 0, 0
    else:
        for f in os.listdir(path):
            if f.lower().endswith('.gif'):
                gif_files.append(os.path.join(path, f))

    if not gif_files:
        print("未找到GIF文件")
        return 0, 0

    # 确定输出目录
    if output_dir:
        output_dir = os.path.expanduser(output_dir)
    else:
        if os.path.isfile(path):
            output_dir = os.path.join(os.path.dirname(path), 'split_output')
        else:
            output_dir = os.path.join(path, 'split_output')

    if not info_only:
        os.makedirs(output_dir, exist_ok=True)

    # 处理每个GIF
    total_files = 0
    total_output = 0

    for gif_path in gif_files:
        try:
            info = get_gif_info(gif_path)

            if info_only:
                print_gif_info(info, max_frames)
            else:
                output_files = split_gif(info, output_dir, max_frames)
                total_output += len(output_files)

            total_files += 1
        except Exception as e:
            print(f"处理失败 {os.path.basename(gif_path)}: {e}")

    if not info_only and total_output > 0:
        print(f"\n✅ 完成！共处理 {total_files} 个文件，生成 {total_output} 个切分文件")
        print(f"   输出目录: {output_dir}")

    return total_files, total_output


def main():
    parser = argparse.ArgumentParser(
        description='GIF动图切分工具 - 将超限GIF拆分成多个小文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s "动图.gif"                    切分单个GIF文件
  %(prog)s ~/Desktop/gifs/              切分文件夹中所有GIF
  %(prog)s "动图.gif" -m 200            自定义最大帧数为200
  %(prog)s "动图.gif" -o ~/output       指定输出目录
  %(prog)s "动图.gif" --info            仅查看GIF信息
'''
    )

    parser.add_argument(
        'path',
        help='GIF文件路径或包含GIF的文件夹路径'
    )

    parser.add_argument(
        '-m', '--max-frames',
        type=int,
        default=280,
        help='每个输出文件的最大帧数（默认: 280，微信公众号限制300帧）'
    )

    parser.add_argument(
        '-o', '--output',
        help='输出目录（默认: 原目录下的 split_output/）'
    )

    parser.add_argument(
        '--info',
        action='store_true',
        help='仅显示GIF信息，不执行切分'
    )

    args = parser.parse_args()

    process_path(args.path, args.output, args.max_frames, args.info)


if __name__ == '__main__':
    main()
