# https://choosealicense.com 协议查询
import setuptools

with open("README.md", "r",encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-auto-router",# 项目名称，保证它的唯一性，不要跟已存在的包名冲突即可
    version="0.1.1",#程序版本
    author="guapit", # 项目作者
    author_email="guapit@qq.com",#作者邮件
    description="flask restful auto router", # 项目的一句话描述
    long_description=long_description,#加长版描述？
    long_description_content_type="text/markdown",#描述使用Markdown
    url="https://github.com/guapit/flask-auto-router",# 项目地址
    packages=setuptools.find_packages(),#无需修改
    classifiers=[
        "Programming Language :: Python :: 3",#使用Python3
        "Programming Language :: Python :: 3.11",#使用Python3
        "License :: OSI Approved :: MIT License",#开源协议
        "Operating System :: OS Independent",
    ],
)