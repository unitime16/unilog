#!/usr/bin/env python3
"""media/ フォルダの中身を調べて media.json を作る。
.mov は ffmpeg があれば自動で .mp4(1080p以下)に変換する。
使い方:  python3 build.py
"""
import json, os, subprocess, shutil
ROOT = "media"
VID = (".mp4", ".m4v", ".webm")
IMG = (".jpg", ".jpeg", ".png", ".webp", ".gif")
ffmpeg = shutil.which("ffmpeg")

def convert(src):
    dst = os.path.splitext(src)[0] + ".mp4"
    if os.path.exists(dst): return
    if not ffmpeg:
        print("  (ffmpegがないので変換スキップ)", src); return
    print("  変換中:", src)
    subprocess.run([ffmpeg, "-y", "-i", src, "-c:v", "libx264", "-crf", "26",
        "-vf", "scale=-2:\'min(1080,ih)\'", "-c:a", "aac", "-movflags", "+faststart", dst],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def walk(d):
    files, dirs = [], {}
    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        if name.startswith("."): continue
        if os.path.isdir(p): dirs[name] = walk(p)
        elif name.lower().endswith(".mov"): convert(p)
        elif name.lower().endswith(VID + IMG):
            files.append(os.path.relpath(p, ROOT).replace(os.sep, "/"))
    return dirs if dirs else files

tree = walk(ROOT)
with open("media.json", "w", encoding="utf-8") as f:
    json.dump(tree, f, ensure_ascii=False, indent=1)
print("media.json を作りました")
