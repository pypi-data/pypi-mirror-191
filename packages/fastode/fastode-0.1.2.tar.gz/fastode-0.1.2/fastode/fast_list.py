#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/2/1 14:08
# @Author  : zhangbc0315@outlook.com
# @File    : fast_list.py
# @Software: PyCharm


class FastList:

    @classmethod
    def list_index(cls, long_list: [], short_list: []) -> [(int, int)]:
        if len(short_list) == 0:
            return []
        if len(long_list) < len(short_list):
            raise ValueError(f"length of long_list({len(long_list)}) is short than short_list({len(short_list)})")
        sl = len(short_list)
        results = []
        for n, value in enumerate(long_list[:-sl+1]):
            if value == short_list[0] and long_list[n:n+sl] == short_list:
                results.append((n, n+sl))
        return results


if __name__ == "__main__":
    pass
