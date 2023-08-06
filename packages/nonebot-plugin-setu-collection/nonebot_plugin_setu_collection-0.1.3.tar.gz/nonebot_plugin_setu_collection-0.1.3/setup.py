from setuptools import setup,find_namespace_packages

setup(
name='nonebot_plugin_setu_collection',
version='0.1.3',
description='从多个api获取色图并根据场景整合的色图插件',
#long_description=open('README.md','r').read(),
author='karisaya',
author_email='1048827424@qq.com',
license='MIT license',
include_package_data=True,
packages=find_namespace_packages(include=["nonebot_plugin_setu_collection","nonebot_plugin_setu_collection.*"]),
platforms='all',
install_requires=["nonebot2","nonebot-adapter-onebot","httpx",],
url='https://github.com/KarisAya/nonebot_plugin_setu_collection',
)