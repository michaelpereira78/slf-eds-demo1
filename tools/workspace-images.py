#!/usr/bin/env python3
"""Hero photos for the Sun Life-styled Advisor workspace and Supervisor console (/advisor, /admin).
Pexels licence; credits in docs/PHOTO-CREDITS.md. Usage: python3 tools/workspace-images.py"""
import os
import subprocess

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'images', 'photos')


def pexels(pid):
    cache = f'/tmp/px2400-{pid}.jpg'
    if not os.path.exists(cache):
        url = f'https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=2400'
        subprocess.run(['curl', '-sSfL', '-o', cache, url], check=True)
    return Image.open(cache).convert('RGB')


def save(im, name):
    im.save(os.path.join(OUT, f'{name}.jpg'), 'JPEG', quality=80, optimize=True, progressive=True)
    print('wrote', name, im.size)


if __name__ == '__main__':
    # full-bleed 1440 x 520 banner ratio (2.77:1); subjects sit right of the text panel
    save(ImageOps.fit(pexels(5198239), (2400, 866), Image.LANCZOS, centering=(0.5, 0.08)), 'ws-advisor-hero')
    save(ImageOps.fit(pexels(8069399), (2400, 866), Image.LANCZOS, centering=(0.5, 0.3)), 'ws-admin-hero')
