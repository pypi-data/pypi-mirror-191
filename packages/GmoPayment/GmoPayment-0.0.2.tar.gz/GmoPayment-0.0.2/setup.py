import setuptools

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='GmoPayment',
    version="0.0.2",
    author="Yaşar Özyurt",
    keywords="GmoPayment",
    author_email="blueromans@gmail.com",
    description='Python API Client for GMO Payment Gateway',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blueromans/GmoPayment.git',
    project_urls={
        "Bug Tracker": "https://github.com/blueromans/GmoPayment/issues",
    },
    packages=['GmoPayment'],
    install_requires=['requests', 'six', 'typing'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
