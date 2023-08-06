from setuptools import setup

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

VERSION = '1.1'
DESCRIPTION = 'Topsis package for MCDM problems'
AUTHOR = 'Rohit Banyal'
AUTHOR_EMAIL = 'rohitbanyal2202@gmail.com'

setup(
    name="Topsis-Rohit-102016087",
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=["Topsis_Rohit_102016087"],
    include_package_data=True,
    install_requires=['pandas', 'os', 'sys'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    license="MIT",
    entry_points={
        "console_scripts": [
            "topsis = Topsis_Rohit_102016087.102016087:main",
        ]
    }
)
