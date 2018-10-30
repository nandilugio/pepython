import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pepython",
    version="0.2.0",
    description="Simple task automation for projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nandilugio/pepython",
    author="Fernando Stecconi",
    author_email="nandilugio@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pyyaml",
        "subprocess32",
    ],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "pepython = pepython.entrypoints:commandline_entrypoint",
        ]
    }
)

