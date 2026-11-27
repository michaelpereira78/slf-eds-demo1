#!/usr/bin/env python3
"""Build the images for the /michael-pereira/ demo replica.

Sources (Pexels licence, see docs/PHOTO-CREDITS.md) are downloaded from images.pexels.com.
Card graphics and the placeholder headshot are generated here (no third-party artwork).
Usage: python3 tools/michael-pereira/make-images.py
"""
import io
import os
import urllib.request

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'images', 'photos')
SERIF = '/usr/share/fonts/truetype/sand-box/google/Noto Serif/NotoSerif-VariableFont_wdth,wght.ttf'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
CREAM = (255, 248, 224)
TEAL = (24, 74, 88)
YELLOW = (255, 203, 5)


def pexels(pid):
    cache = f'/tmp/px-{pid}.jpg'
    if not os.path.exists(cache):
        url = f'https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=1800'
        with urllib.request.urlopen(url) as r, open(cache, 'wb') as f:
            f.write(r.read())
    return Image.open(cache).convert('RGB')


def local(name):
    return Image.open(os.path.join(OUT, f'{name}.jpg')).convert('RGB')


def save(im, name, q=82):
    im.save(os.path.join(OUT, f'{name}.jpg'), 'JPEG', quality=q, optimize=True, progressive=True)
    print('wrote', name, im.size)


def cover(im, w, h, cx=0.5, cy=0.5):
    return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(cx, cy))


def card(bg, inner, title, name, highlight=None):
    """A social-post style card: blurred photo edges, cream centre panel, serif headline, photo."""
    W, H = 720, 416
    base = cover(bg, W, H).filter(ImageFilter.GaussianBlur(18))
    base = Image.blend(base, Image.new('RGB', (W, H), (245, 238, 220)), 0.25)
    pw, px = 300, (W - 300) // 2
    d = ImageDraw.Draw(base)
    d.rectangle([px, 0, px + pw, H], fill=CREAM)
    d.ellipse([px + 16, 16, px + 30, 30], fill=YELLOW)
    d.text((px + 36, 14), 'Sun Life', font=ImageFont.truetype(SANS_B, 13), fill=TEAL)
    f = ImageFont.truetype(SERIF, 25)
    y = 44
    for line in title:
        if highlight and line == highlight:
            bb = d.textbbox((px + 16, y), line, font=f)
            d.rectangle([bb[0] - 3, bb[1] - 2, bb[2] + 3, bb[3] + 3], fill=YELLOW)
        d.text((px + 16, y), line, font=f, fill=TEAL)
        y += 31
    ph = H - y - 18
    base.paste(cover(inner, pw - 32, ph), (px + 16, y + 6))
    save(base, name)


def headshot():
    S = 480
    im = Image.new('RGB', (S, S), (232, 234, 235))
    d = ImageDraw.Draw(im)
    g = (178, 184, 188)
    d.ellipse([S * 0.32, S * 0.17, S * 0.68, S * 0.53], fill=g)
    d.ellipse([S * 0.14, S * 0.58, S * 0.86, S * 1.25], fill=g)
    save(im, 'mp-headshot-placeholder', 90)


def poster(src, name, dark=0.55, cx=0.5):
    im = cover(src, 1104, 622, cx)
    im = Image.blend(im, Image.new('RGB', im.size, (0, 0, 0)), dark)
    save(im, name)


if __name__ == '__main__':
    walk = pexels(4173151)
    # the family sits right of centre, clear of the cream text panel (as in the reference banner)
    save(cover(walk, 1800, 650, 0.5, 0.6), 'hero-mp-autumn-walk')
    save(cover(pexels(8576088), 1800, 650, 0.5, 0.55), 'hero-mp-boardwalk')
    save(cover(local('advisor-meeting'), 1800, 650, 0.5, 0.4), 'hero-mp-meeting')
    save(cover(local('retirement-walk'), 1800, 650, 0.5, 0.6), 'hero-mp-retirement')
    save(cover(local('couple-planning'), 1800, 650, 0.5, 0.4), 'hero-mp-planning')
    save(cover(pexels(35835482), 1104, 758, 0.5, 0.5), 'mp-coffee')
    save(cover(local('couple-planning'), 1104, 758, 0.5, 0.5), 'mp-planning')
    save(cover(local('advisor-meeting'), 1104, 758, 0.5, 0.5), 'mp-meeting')
    save(cover(pexels(8576088), 1104, 758, 0.5, 0.5), 'mp-family')
    save(cover(local('retirement-walk'), 1104, 758, 0.5, 0.5), 'mp-retirement')
    poster(local('advisor-meeting'), 'mp-video-intro', 0.62)
    poster(local('couple-planning'), 'mp-video-products', 0.15)
    card(walk, walk, ['You\u2019re building', 'a family'], 'mp-card-family')
    card(local('couple-planning'), local('couple-planning'), ['Your wealth tells', 'a story. What\u2019s the', 'next chapter?'],
         'mp-card-wealth', highlight='next chapter?')
    card(local('advisor-meeting'), local('advisor-meeting'), ['6 ways to use your', 'critical illness payout'], 'mp-card-cii')
    card(local('retirement-walk'), local('retirement-walk'), ['Retirement is a', 'journey, not a date'], 'mp-card-retirement')
    card(pexels(35835482), pexels(35835482), ['Small habits,', 'big savings'], 'mp-card-budget')
    headshot()
