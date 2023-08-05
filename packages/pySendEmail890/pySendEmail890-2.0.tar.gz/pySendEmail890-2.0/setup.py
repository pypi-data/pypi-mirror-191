# -- coding: utf-8 --
# @Time : 2023/2/10 16:25
# @Author : xjt
# @Email :1165423664@qq.com
# @File : setup.py
# @Software: PyCharm
import setuptools

setuptools.setup(
    name='pySendEmail890',
    version='2.0',
    author='xjt',
    author_email='1165423664@qq.com',
    description='邮件发送封装，定时抄送附近多人',
    long_description_content_type="""text/markdown""",
    url='https://gitee.com/demon000/hongruan.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
