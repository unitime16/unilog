#!/usr/bin/env python3
import json, os, subprocess, shutil
ROOT = "media"
VID = (".mp4", ".m4v", ".webm")
IMG = (".jpg", ".jpeg", ".png", ".webp", ".gif")
ffmpeg = shutil.which("ffmpeg")

def convert(src):
    dst = os.path.splitext(src)[0] + ".mp4"
    if os.path.exists(dst): return
    if not ffmpeg:
        print("  (ffmpegがないので、.movのまま使います)", src); return
    print("  変換中:", src)
    subprocess.run([ffmpeg, "-y", "-i", src, "-c:v", "libx264", "-crf", "26",
        "-vf", "scale=-2:'min(1080,ih)'", "-c:a", "aac", "-movflags", "+faststart", dst],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def walk(d):
    files, dirs = [], {}
    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        if name.startswith("."): continue
        if os.path.isdir(p):
            dirs[name] = walk(p)
        elif name.lower().endswith(".mov"):
            convert(p)
            if not os.path.exists(os.path.splitext(p)[0] + ".mp4"):
                files.append(os.path.relpath(p, ROOT).replace(os.sep, "/"))
        elif name.lower().endswith(VID + IMG):
            files.append(os.path.relpath(p, ROOT).replace(os.sep, "/"))
    return dirs if dirs else files

tree = walk(ROOT)
with open("media.js", "w", encoding="utf-8") as f:
    f.write("const TREE = " + json.dumps(tree, ensure_ascii=False, indent=1) + ";")
print("media.js を作りました")
