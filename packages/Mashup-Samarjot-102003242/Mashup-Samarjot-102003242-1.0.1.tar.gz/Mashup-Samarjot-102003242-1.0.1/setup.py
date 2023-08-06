from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="Mashup-Samarjot-102003242",
    version="1.0.1",
    description="Python package creating Mashup of multiple songs.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Samarjot Singh",
    author_email="2001samar@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    packages=["Mashup"],
    include_package_data=True,
    install_requires=['pytube',
                      'pydub',
     ],
     entry_points={
        "console_scripts": [
            "mashup=Mashup.__main__:main",
        ]
     },
)