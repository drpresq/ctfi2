from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_desc = fh.read()

setup(
    name='ctfi2',
    version="1.5.4",
    packages=["ctfi2", "ctfi2.api", "ctfi2.gui", "ctfi2.gui.components", "ctfi2.cli"],
    package_dir={'': "src"},
    scripts=['scripts/ctfi2'],
    author="George",
    author_email="drpresq@gmail.com",
    description="ctfi2 - CTFd Interface 2",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/drpresq/ctfi2",
    install_requires=[
        "requests>=2.22.0",
        "PyQt5>=5.9.2",
        "simplejson>=3.16.0",
        "setuptools>=45.2.0"
    ],
    keywords="",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities'
    ],
)

"""
    project_urls={
        "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://code.example.com/HelloWorld/",
    },
"""

