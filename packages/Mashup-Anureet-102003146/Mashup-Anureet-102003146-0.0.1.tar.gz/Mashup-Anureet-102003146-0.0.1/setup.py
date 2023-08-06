from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="Mashup-Anureet-102003146",
    version="0.0.1",
    description="Mashup in Python.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Anureet Kaur",
    author_email="akaur7_be20@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Mashup_Py"],
    include_package_data=True,
    install_requires=['pytube',
                      'pydub'
     ],
    
)
