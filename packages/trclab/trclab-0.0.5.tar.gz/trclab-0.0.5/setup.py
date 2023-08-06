from setuptools import setup, find_packages

VERSION = "0.0.5"
DESCRIPTION = 'STUST TRCLab Package'
LONG_DESCRIPTION = 'This is STUST TRCLab Package.'

setup(
    name="trclab",
    version=VERSION,
    author="STUST-TRCLab",
    author_email="mb1g0110@stust.edu.tw",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['trclab', 'stust'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Traditional)",
        "Programming Language :: Python :: 3.8",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ]
)
