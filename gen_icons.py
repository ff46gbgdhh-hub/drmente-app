#!/usr/bin/env python3
"""Gera os icones PWA do Dr. Mente (alvo/meta em gradiente roxo)."""
from PIL import Image, ImageDraw


def make_icon(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Gradiente roxo diagonal (#7c5cbf -> #5a3d9a)
    c1 = (124, 92, 191)
    c2 = (90, 61, 154)
    for y in range(size):
        t = y / size
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        d.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Cantos arredondados (nao-maskable). Maskable = quadrado cheio p/ safe-zone.
    if not maskable:
        radius = int(size * 0.22)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [0, 0, size - 1, size - 1], radius=radius, fill=255)
        img.putalpha(mask)
        d = ImageDraw.Draw(img)

    # Alvo (meta): aneis concentricos brancos
    cx = cy = size / 2
    inset = size * (0.30 if maskable else 0.22)
    outer = size / 2 - inset
    ring = outer / 3.0
    white = (255, 255, 255, 255)
    accent = (212, 160, 200, 255)  # --accent rosado

    for i, rr in enumerate([outer, outer - ring, outer - 2 * ring]):
        col = white if i % 2 == 0 else accent
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
        inner = rr - ring
        if inner > 0:
            # recorta o centro pra formar o anel (exceto o miolo final)
            grad_c = (
                int(c1[0] + (c2[0] - c1[0]) * (cy / size)),
                int(c1[1] + (c2[1] - c1[1]) * (cy / size)),
                int(c1[2] + (c2[2] - c1[2]) * (cy / size)),
                255,
            )
            if i < 2:
                d.ellipse([cx - inner, cy - inner, cx + inner, cy + inner],
                          fill=grad_c)

    # Miolo central
    core = ring * 0.62
    d.ellipse([cx - core, cy - core, cx + core, cy + core], fill=white)
    return img


for s in (192, 512):
    make_icon(s).save(f"icon-{s}.png")
make_icon(512, maskable=True).save("icon-512-maskable.png")
print("icones gerados: icon-192.png, icon-512.png, icon-512-maskable.png")
