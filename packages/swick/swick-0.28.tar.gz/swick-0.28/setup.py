from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name="swick",
    version="0.28",
    description="The slick way to process SWC files.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Nathan T. Spencer",
    author_email="nathantspencer@gmail.com",
    url="https://nathantspencer.com",
    python_requires=">=3.**",
    install_requires=[''],
    packages=['swick'],
    package_data={
        '': [''],
    },
    classifiers=[
        'Development Status :: 4 - Beta'
    ]
)
