import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyxk",
    version="0.1.9",
    author="xk",
    install_requires=[
        "yarl",
        "requests",
        "pycryptodome",
        "rich",
        "m3u8",
        "aiohttp",
        "aiofiles",
    ],
    entry_points={
        'console_scripts': [
            'm3u8 = pyxk.m3u8.entry_points:main',
        ],
    },
    author_email="925330867@qq.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)