[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pylint](https://img.shields.io/badge/pylint-9.97-ffbf48)](https://pylint.pycqa.org/en/latest/)
[![License](https://img.shields.io/badge/license-LGPL--2.1-a32d2a)](https://spdx.org/licenses/LGPL-2.1-only.html)
[![PyPi](https://img.shields.io/pypi/v/hqx)](https://pypi.org/project/hqx/)

<img src="logo.png" width=80 align="right"></img>

**hqx** *(high quality scale)* is a family of pixel art scaling algorithms that work
by detecting differences between pixels in the [YUV](https://en.wikipedia.org/wiki/YUV) colorspace.

**hq2x** scales an image by 2x, **hq3x** by 3x, and **hq4x** by 4x.

__This is a Python port of hqx, unoptimized.__
It is not intended to be used for videos or scenarios where low latency is required.
Right now, it only supports RGB, not RGB**A** (no transparency support).

---

## Table of contents
- [📦 Installation](#-installation)
- [🛠 Usage](#-usage)
- [📰 Changelog](#-changelog)
- [📜 License](#-license)

---

## 📦 Installation

`hqx` is available on PyPi.
It requires a Python version of **at least 3.10.0.**
It depends on [Pillow](https://pypi.org/project/Pillow/).

To install `hqx` with pip, run:
```shell
python -m pip install hqx
```

---

## 🛠 Usage

You can either use `hqx.hqx_scale`, `hqx.hq2x`, `hqx.hq3x`, or `hqx.hq4x`.

```python
import hqx
import PIL.Image

image: PIL.Image.Image = PIL.Image.open(...)
x2:    PIL.Image.Image = hqx.hq2x(image)
x3:    PIL.Image.Image = hqx.hq3x(image)
x4:    PIL.Image.Image = hqx.hq4x(image)

# x2 == hqx.hqx_scale(image, 2))
# x3 == hqx.hqx_scale(image, 3))
# x4 == hqx.hqx_scale(image, 4))
```

---

## 📰 Changelog

The changelog is at [CHANGELOG.md](CHANGELOG.md).

---

## 📜 License

hqx (python) is licensed under the [Lesser GNU Public License v2.1 (LGPL-2.1)](https://spdx.org/licenses/LGPL-2.1-only.html).