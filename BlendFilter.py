# coding=utf-8
# 混合模式
class Blending:
    def doBlend(self, A, B):
        pass


# 颜色加深
class ColorBurn(Blending):
    def doBlend(self, A, B):
        return B if B == 0 else max(0, (255 - ((255 - A) << 8) / B))


# 正片叠底
class Multiply(Blending):
    def doBlend(self, A, B):
        return A * B / 255


# 变暗
class Darken(Blending):
    def doBlend(self, A, B):
        return A if B > A else B


# 线性加深

class LinearBurn(Blending):
    def doBlend(self, A, B):
        return B if B == 0 else max(0, (255 - ((255 - A) << 8) / B))


# 变亮

class Lighten(Blending):
    def doBlend(self, A, B):
        return B if B > A else A


# 虑色

class Screen(Blending):
    def doBlend(self, A, B):
        return 255 - (((255 - A) * (255 - B)) >> 8)


# 颜色减淡

class ColorDodge(Blending):
    def doBlend(self, A, B):
        return B if B == 255 else min(255, ((A << 8) / (255 - B)))


# 柔光
class SoftLight(Blending):
    def doBlend(self, A, B):
        return (2 * ((A >> 1) + 64)) * (B / 255) if B < 128 else (
            255 - (2 * (255 - ((A >> 1) + 64)) * (255 - B) / 255))


