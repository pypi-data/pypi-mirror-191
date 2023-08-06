import setuptools
 
requirements = [
    "python-snap7==1.3",
    "docker==6.0.1",
    "modbus_tk==1.1.2",
    "pyModbusTCP==0.2.0",
    "pyinstaller==5.7.0",
    "sqlalchemy==2.0.3",
    "tortoise-orm==0.19.3",
    "gitpython==3.1.30",
    "requests==2.28.2",
    "pymysql==1.0.2",
    "redis==4.5.1",
    "pywin32==305"
]       # 自定义工具中需要的依赖包
 
setuptools.setup(
    name="Bruce_li_one",       # 自定义工具包的名字
    version="0.0.8",             # 版本号
    author="Bruce_li123",           # 作者名字
    author_email="lws__xinlang@sina.com",  # 作者邮箱
    description="description", # 自定义工具包的简介
    license='MIT-0',           # 许可协议
    url="",              # 项目开源地址
    packages=setuptools.find_packages(),  # 自动发现自定义工具包中的所有包和子包
    install_requires=requirements,  # 安装自定义工具包需要依赖的包
    python_requires='>=3.5'         # 自定义工具包对于python版本的要求
)