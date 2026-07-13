#!/usr/bin/env python3
"""
Download semua gambar + video Regent Residence dari Cloudways → Convert ke WebP.
Video tetap .mov (tidak di-convert).
Jalankan: python download_images.py
"""

import os
import requests
from PIL import Image
from io import BytesIO

IMAGE_MAP = {
    # Logo & Monogram
    "https://regent-jakarta.co/wp-content/uploads/2025/08/regent-jakarta.png": "regent-logo.webp",
    "https://regent-jakarta.co/wp-content/uploads/2025/08/Regent-Monogram-Teal-2.png": "regent-monogram.webp",

    # Concept
    "https://regent-jakarta.co/wp-content/uploads/2025/08/Regent-Website-8.jpg": "regent-concept.webp",

    # Unit Types
    "https://regent-jakarta.co/wp-content/uploads/2025/08/unittypes2.png": "regent-unit-types.webp",

    # Show Unit
    "https://regent-jakarta.co/wp-content/uploads/2025/08/Regent-Residence-Jakarta-Moie-Show-Unit-2.jpg": "regent-moie-showunit.webp",

    # Location Map
    "https://regent-jakarta.co/wp-content/uploads/2025/08/map-regent.jpg": "regent-map.webp",

    # Gallery / Viewing
    "https://regent-jakarta.co/wp-content/uploads/2025/09/Regent-Residence-Jakarta-39-1.jpg": "regent-viewing.webp",
    "https://regent-jakarta.co/wp-content/uploads/2025/09/Regent-Residence-Jakarta-21-2.jpg": "regent-gallery-1.webp",
    "https://regent-jakarta.co/wp-content/uploads/2025/09/Regent-Residence-Jakarta-6-2.jpg": "regent-gallery-2.webp",

    # Featured Image (from og:image / elementor config)
    "https://regent-jakarta.co/wp-content/uploads/2025/08/regent-residence-jakarta-37.jpg": "regent-hero-fallback.webp",
}

# Video (download as-is, no conversion)
VIDEO_MAP = {
    "https://regent-jakarta.co/wp-content/uploads/2025/08/Landscape-Magran-33N.mov": "regent-hero-video.mov",
}

MAX_WIDTH = 1600
WEBP_QUALITY = 82

def download_and_convert(url, filename):
    try:
        print(f"  {filename}...", end=" ", flush=True)
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            img = img.resize((MAX_WIDTH, int(img.height * ratio)), Image.LANCZOS)
        img.save(filename, "WEBP", quality=WEBP_QUALITY)
        print(f"✅ {img.width}x{img.height} → {os.path.getsize(filename)/1024:.0f} KB")
        return True
    except Exception as e:
        print(f"❌ {e}")
        return False

def download_video(url, filename):
    try:
        print(f"  {filename}...", end=" ", flush=True)
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=120, stream=True)
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"✅ {size_mb:.1f} MB")
        return True
    except Exception as e:
        print(f"❌ {e}")
        return False

def main():
    total_img = len(IMAGE_MAP)
    total_vid = len(VIDEO_MAP)
    ok = 0

    print(f"\n  Regent Residence → Image Downloader")
    print(f"  {total_img} images + {total_vid} video\n")

    print("  --- Images (→ WebP) ---")
    for url, fn in IMAGE_MAP.items():
        if download_and_convert(url, fn):
            ok += 1

    print("\n  --- Video (→ .mov as-is) ---")
    for url, fn in VIDEO_MAP.items():
        if download_video(url, fn):
            ok += 1

    print(f"\n  Done: {ok}/{total_img + total_vid} files.\n")

if __name__ == "__main__":
    main()
