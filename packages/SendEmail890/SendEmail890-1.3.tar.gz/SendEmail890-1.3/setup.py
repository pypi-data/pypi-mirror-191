# -- coding: utf-8 --
# @Time : 2023/2/10 16:25
# @Author : xjt
# @Email :1165423664@qq.com
# @File : setup.py
# @Software: PyCharm
import setuptools

setuptools.setup(
    name='SendEmail890',
    version='1.3',
    author='xjt',
    author_email='1165423664@qq.com',
    description='对openpyxl和lxrd进行二次开发,实现excel序列化',
    long_description_content_type="""text/markdown""",
    url='https://gitee.com/demon000/hongruan.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
          'smtplib','email'
      ]
)
