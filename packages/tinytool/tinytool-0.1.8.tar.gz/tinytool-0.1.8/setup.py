import os
import codecs
import setuptools

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding='utf-8') as fh:
    long_description = "\\n" + fh.read()

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="tinytool",
    version="0.1.8",
    # version="0.0.6",
    author="leeheisen",
    author_email="leeheisen@126.com",
    description="A tiny tool for personal use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leeHeisen/TinyTool.git",
    project_urls={
        "Bug Tracker": "https://github.com/leeHeisen/TinyTool/issues",
    },
    install_requires=['xlwings', 'json5', 'pytz'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)


# setup(
#     name='tinytool',
#     version='0.0.1',
#     description=(
#         'This is a tool for personal use'
#     ),
#     long_description=open('README.md', 'r', encoding='utf-8').read(),
#     long_description_content_type="text/markdown",
#     author='leeheisen',
#     author_email='leeheisen@126.com',
#     maintainer='leeheisen',
#     maintainer_email='leeheisen@126.com',
#     license='MIT License',
#     packages=find_packages(),
#     platforms=["all"],
#     url='https://github.com/leeHeisen/TinyTool.git',
#     classifiers=[
#         # 'Development Status :: 4 - Beta',
#         'Operating System :: OS Independent',
#         'Intended Audience :: Developers',
#         'License :: OSI Approved :: BSD License',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: Implementation',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.4',
#         'Programming Language :: Python :: 3.5',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: 3.7',
#         'Topic :: Software Development :: Libraries'
#     ],
#     install_requires=[
#         # "boto3 >= 1.17.0",
#         "requests >= 2.12.1",
#     ]
# )
