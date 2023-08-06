from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.2.22'
DESCRIPTION = 'Narrating Accounting! using Python.用python进行会计叙事。'

# Setting up
setup(
    name="cpanlp",
    version=VERSION,
    author="Draco Deng",
    author_email="dracodeng6@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://cpanlp.com",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'accounting', 'cpa', 'audit','intelligent accounting', 'linguistic turn', 'linguistic',"intelligent audit","natural language processing","machine learning","finance","certified public accountant",'big four',"会计","注会","注册会计师","审计","智能会计","会计的语言学转向","语言学","智能审计","自然语言处理","机器学习","金融","北外","财会","四大","注册会计"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)