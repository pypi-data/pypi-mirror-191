# zxtools

#### 介绍
zx的一个工具集，以Python为主，

#### 安装教程

1.  python -m pip install .
2.  python -m pip install zxt
3.  python -m pip install --upgrade zxt

#### 上传教程

1.  创建 .pypirc 文件
    type NUL > %UserProfile%\.pypirc

2.  pypirc 规范
    https://packaging.python.org/specifications/pypirc/

3.  升级工具
    python -m pip install --upgrade build
    python -m pip install --upgrade twine

4.  Generating distribution archives (生成档案)
    https://packaging.python.org/en/latest/tutorials/packaging-projects/
    切换到 pyproject.toml 的同级目录
    python -m build

5.  Uploading the distribution archives (上传档案)
    https://packaging.python.org/en/latest/tutorials/packaging-projects/
    python -m twine upload --repository zxt dist/*
