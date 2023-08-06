#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: LGPL-2.1-only
"""
**hqx** *(high quality scale)* is a family of pixel art scaling algorithms that work
by detecting differences between pixels in the `YUV <https://en.wikipedia.org/wiki/YUV>`_ colorspace.

**hq2x** scales an image by 2x, **hq3x** by 3x, and **hq4x** by 4x.

This is a Python port of hqx, unoptimized.
It is not intended to be used for videos or scenarios where low latency is required.

----

You can either use ```hqx.hqx_scale``, ``hqx.hq2x``, ``hqx.hq3x``, or ``hqx.hq4x``.

>>> import hqx
>>> import PIL.Image
>>> image: PIL.Image.Image = PIL.Image.open(...)
>>> x2:    PIL.Image.Image = hqx.hq2x(image)
>>> x3:    PIL.Image.Image = hqx.hq3x(image)
>>> x4:    PIL.Image.Image = hqx.hq4x(image)
>>> # x2 == hqx.hqx_scale(image, 2))
>>> # x3 == hqx.hqx_scale(image, 3))
>>> # x4 == hqx.hqx_scale(image, 4))

----

hqx (python) is licensed under the
`Lesser GNU Public License v2.1 (LGPL-2.1) <https://spdx.org/licenses/LGPL-2.1-only.html>`_.
"""
import functools
import PIL.Image
import PIL.PyAccess

import hqx.rgb_yuv
import hqx.algor_hq2x
import hqx.algor_hq3x
import hqx.algor_hq4x

__version__ = "1.0"
__author__ = "WhoAteMyButter"


def hqx_scale(image: PIL.Image.Image, scale: int) -> PIL.Image.Image:
    if scale not in (2, 3, 4):
        raise ValueError("scale must be 2, 3, or 4")
    if scale == 2:
        return hq2x(image)
    if scale == 3:
        return hq3x(image)
    if scale == 4:
        return hq4x(image)
    # This should never happen, just return the image
    return image


def hq2x(image: PIL.Image.Image) -> PIL.Image.Image:
    """
    Scale `image` according to hq2x.
    The returned image will be 2*W, 2*H.

    :param image: An instance of ``PIL.Image.Image``.
    :return: A hq2x scaled version of `image`.
    """
    width, height = image.size
    source = image.convert("RGB")
    dest = PIL.Image.new("RGB", (width * 2, height * 2))

    # These give direct pixel access via grid[x_coord, y_coord]
    sourcegrid: PIL.PyAccess.PyAccess = source.load()
    destgrid: PIL.PyAccess.PyAccess = dest.load()

    @functools.cache
    def get_px(x_coord: int, y_coord: int) -> tuple[int, int, int]:
        if x_coord < 0:
            x_coord = 0
        elif x_coord >= width:
            x_coord = width - 1

        if y_coord < 0:
            y_coord = 0
        elif y_coord >= height:
            y_coord = height - 1

        return sourcegrid[x_coord, y_coord]

    for x in range(width):
        for y in range(height):
            pixel = hqx.algor_hq2x.hq2x_pixel(
                [
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x - 1, y - 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x, y - 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x + 1, y - 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x - 1, y)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x, y)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x + 1, y)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x - 1, y + 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x, y + 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x + 1, y + 1)),
                ]
            )

            x_scaled = x * 2
            y_scaled = y * 2

            destgrid[x_scaled, y_scaled] = hqx.rgb_yuv.packed_int_to_tuple(pixel[0])
            destgrid[x_scaled + 1, y_scaled] = hqx.rgb_yuv.packed_int_to_tuple(pixel[1])
            destgrid[x_scaled, y_scaled + 1] = hqx.rgb_yuv.packed_int_to_tuple(pixel[2])
            destgrid[x_scaled + 1, y_scaled + 1] = hqx.rgb_yuv.packed_int_to_tuple(pixel[3])

    return dest


def hq3x(image: PIL.Image.Image) -> PIL.Image.Image:
    """
    Scale `image` according to hq3x.
    The returned image will be 3*W, 3*H.

    :param image: An instance of ``PIL.Image.Image``.
    :return: A hq3x scaled version of `image`.
    """
    width, height = image.size
    source = image.convert("RGB")
    destination = PIL.Image.new("RGB", (width * 3, height * 3))

    # These give direct pixel access via grid[x_coord, y_coord]
    sourcegrid: PIL.PyAccess.PyAccess = source.load()
    destgrid: PIL.PyAccess.PyAccess = destination.load()

    @functools.cache
    def get_px(x_coord: int, y_coord: int) -> tuple[int, int, int]:
        if x_coord < 0:
            x_coord = 0
        elif x_coord >= width:
            x_coord = width - 1

        if y_coord < 0:
            y_coord = 0
        elif y_coord >= height:
            y_coord = height - 1

        return sourcegrid[x_coord, y_coord]

    for x in range(width):
        for y in range(height):
            pixel = hqx.algor_hq3x.hq3x_pixel(
                [
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x - 1, y - 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x, y - 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x + 1, y - 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x - 1, y)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x, y)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x + 1, y)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x - 1, y + 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x, y + 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x + 1, y + 1)),
                ]
            )

            x_scaled = x * 3
            y_scaled = y * 3

            destgrid[x_scaled, y_scaled] = hqx.rgb_yuv.packed_int_to_tuple(pixel[0])
            destgrid[x_scaled + 1, y_scaled] = hqx.rgb_yuv.packed_int_to_tuple(pixel[1])
            destgrid[x_scaled + 2, y_scaled] = hqx.rgb_yuv.packed_int_to_tuple(pixel[2])
            destgrid[x_scaled, y_scaled + 1] = hqx.rgb_yuv.packed_int_to_tuple(pixel[3])
            destgrid[x_scaled + 1, y_scaled + 1] = hqx.rgb_yuv.packed_int_to_tuple(pixel[4])
            destgrid[x_scaled + 2, y_scaled + 1] = hqx.rgb_yuv.packed_int_to_tuple(pixel[5])
            destgrid[x_scaled, y_scaled + 2] = hqx.rgb_yuv.packed_int_to_tuple(pixel[6])
            destgrid[x_scaled + 1, y_scaled + 2] = hqx.rgb_yuv.packed_int_to_tuple(pixel[7])
            destgrid[x_scaled + 2, y_scaled + 2] = hqx.rgb_yuv.packed_int_to_tuple(pixel[8])

    return destination


def hq4x(image: PIL.Image.Image) -> PIL.Image.Image:
    width, height = image.size
    source = image.convert("RGB")
    destination = PIL.Image.new("RGB", (width * 4, height * 4))

    # These give direct pixel access via grid[x_coord, y_coord]
    sourcegrid: PIL.PyAccess.PyAccess = source.load()
    destgrid: PIL.PyAccess.PyAccess = destination.load()

    @functools.cache
    def get_px(x_coord: int, y_coord: int) -> tuple[int, int, int]:
        if x_coord < 0:
            x_coord = 0
        elif x_coord >= width:
            x_coord = width - 1

        if y_coord < 0:
            y_coord = 0
        elif y_coord >= height:
            y_coord = height - 1

        return sourcegrid[x_coord, y_coord]

    for x in range(width):
        for y in range(height):
            pixel = hqx.algor_hq4x.hq4x_pixel(
                [
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x - 1, y - 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x, y - 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x + 1, y - 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x - 1, y)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x, y)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x + 1, y)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x - 1, y + 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x, y + 1)),
                    hqx.rgb_yuv.tuple_to_packed_int(get_px(x + 1, y + 1)),
                ]
            )

            x_scaled = x * 4
            y_scaled = y * 4

            destgrid[x_scaled, y_scaled] = hqx.rgb_yuv.packed_int_to_tuple(pixel[0])
            destgrid[x_scaled + 1, y_scaled] = hqx.rgb_yuv.packed_int_to_tuple(pixel[1])
            destgrid[x_scaled + 2, y_scaled] = hqx.rgb_yuv.packed_int_to_tuple(pixel[2])
            destgrid[x_scaled + 3, y_scaled] = hqx.rgb_yuv.packed_int_to_tuple(pixel[3])

            destgrid[x_scaled, y_scaled + 1] = hqx.rgb_yuv.packed_int_to_tuple(pixel[4])
            destgrid[x_scaled + 1, y_scaled + 1] = hqx.rgb_yuv.packed_int_to_tuple(pixel[5])
            destgrid[x_scaled + 2, y_scaled + 1] = hqx.rgb_yuv.packed_int_to_tuple(pixel[6])
            destgrid[x_scaled + 3, y_scaled + 1] = hqx.rgb_yuv.packed_int_to_tuple(pixel[7])

            destgrid[x_scaled, y_scaled + 2] = hqx.rgb_yuv.packed_int_to_tuple(pixel[8])
            destgrid[x_scaled + 1, y_scaled + 2] = hqx.rgb_yuv.packed_int_to_tuple(pixel[9])
            destgrid[x_scaled + 2, y_scaled + 2] = hqx.rgb_yuv.packed_int_to_tuple(pixel[10])
            destgrid[x_scaled + 3, y_scaled + 2] = hqx.rgb_yuv.packed_int_to_tuple(pixel[11])

            destgrid[x_scaled, y_scaled + 3] = hqx.rgb_yuv.packed_int_to_tuple(pixel[12])
            destgrid[x_scaled + 1, y_scaled + 3] = hqx.rgb_yuv.packed_int_to_tuple(pixel[13])
            destgrid[x_scaled + 2, y_scaled + 3] = hqx.rgb_yuv.packed_int_to_tuple(pixel[14])
            destgrid[x_scaled + 3, y_scaled + 3] = hqx.rgb_yuv.packed_int_to_tuple(pixel[15])
    return destination
