#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/11/1 18:41
# @Author  : zhangbc0315@outlook.com
# @File    : fast_color.py
# @Software: PyCharm


class FastColor:

    @classmethod
    def _get_r_func_from_range(cls, min_v, max_v):
        x1 = (max_v + min_v) / 2
        k = - 255 / (x1 - min_v)
        b = - k * x1

        def r_func(v):
            return max(k * v + b, 0)

        return r_func

    @classmethod
    def _get_g_func_from_range(cls, min_v, max_v):
        x1 = (max_v + min_v) / 2
        k = 255 / (x1 - min_v)
        b = 255 - k * x1

        def g_func(v):
            res = abs(k * v + b)
            if v > x1:
                res = 510 - res
            return res
        return g_func

    @classmethod
    def _get_b_func_from_range(cls, min_v, max_v):
        x0 = (min_v + max_v) / 2
        x1 = max_v
        y0 = 0
        y1 = 255
        k = (y1 - y0) / (x1 - x0)
        b = y1 - k * x1

        def b_func(v):
            return max(k * v + b, 0)

        return b_func

    @classmethod
    def get_rgbs(cls, min_v, max_v, gap):
        r_f = cls._get_r_func_from_range(min_v, max_v)
        g_f = cls._get_g_func_from_range(min_v, max_v)
        b_f = cls._get_b_func_from_range(min_v, max_v)
        vs = list(range(min_v, max_v, gap))
        rs = [r_f(v) for v in vs]
        gs = [g_f(v) for v in vs]
        bs = [b_f(v) for v in vs]
        return list(zip(rs, gs, bs))

    @classmethod
    def _num_to_hex(cls, num):
        color_num = int(num)
        ch = hex(color_num)[2:]
        if len(ch) == 1:
            return '0' + ch
        else:
            return ch

    @classmethod
    def rgb_to_hex(cls, rgb):
        r = cls._num_to_hex(rgb[0])
        g = cls._num_to_hex(rgb[1])
        b = cls._num_to_hex(rgb[2])
        return f"#{r}{g}{b}"


if __name__ == "__main__":
    pass
