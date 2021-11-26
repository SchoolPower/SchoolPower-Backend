#!/bin/bash
chmod +x ./bootstrap
pip uninstall enum34
pip install -t . -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
