from setuptools import setup, find_packages

setup(
    name = 'coloriran',
    version = '1.0',
    author='mohammad saeed salari',
    author_email = 'salari601601@gmail.com',
    description = 'A library to color your codes',
    keywords = ['color', 'colorama', 'colors', 'Fore', 'culor', 'colur', 'culor', 'culurs'],
    long_description = open("README.md", encoding="utf-8").read(),
    python_requires="~=3.7",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/mrsalari/coloriran',
    packages = find_packages(),
    classifiers = [
    	"Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ]
)