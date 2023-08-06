from setuptools import setup

setup(
    name = 'LibrarySwift',
    version = '1.0.0',
    author = 'Mohamad_Dark',
    author_email = 'mr.mohamad.dark@gmail.com',
    description = 'Swift Rubika is a simple and fast Rubika Messenger library built for you',
    license = "MIT",
    keywords = ["Swiftlibrary","messenger","python2","python","python3","api","self","Rubx","Rubika", "SwiftRubika","rubix","rubikax","rubika","bot","robot","library","rubikalib","rubikalibrary","rubika.ir","librarySwiftRubika","m.rubika.ir"],
    long_description = open('README.rst').read(),
    python_requires = "~=3.7",
    long_description_content_type = 'text/x-rst',
    url = 'https://github.com/mester-root/rubx',
    packages = ['LibrarySwift'],
    install_requires = ["requests", "urllib3", "pycryptodome","colorama","tinytag"],
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