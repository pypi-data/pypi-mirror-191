from setuptools import setup, find_packages

setup(
    name="fish_tool",
    version="1.0",
    author="aifish",
    url="https://gitee.com/laowangzi/fish_tool",
    author_email="ofyu@163.com",
    description="some tool code",
    packages=find_packages(),
    install_requires=[
        'pyyaml>=6.0',
        'tqdm>=4.36.1',
        'requests>=2.22.0',
        'httpx>=0.18.1',
        "fastapi>=0.90.0",
        "uvicorn>=0.20.0",
    ],
    extras_require={
        'AI': [
            "torch>=1.0"
        ],
        'db': [
            "pymysql>=1.0.2"
        ],
    },
    python_requires='>=3.6',
)
