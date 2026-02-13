from setuptools import setup

# 读取 requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='video-extraction',
    version='1.0.0',
    description='Video text extraction workflow',
    install_requires=requirements,
    python_requires='>=3.12',
)
