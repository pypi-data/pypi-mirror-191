import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mcalpy",
    version="0.0.7",
    author="seoggeonjins",
    author_email="seoggeonjin@gmail.com",
    description="A small my math program\nIt has little math functions",

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seoggeonjin/MAIN",
    download_url="https://github.com/seoggeonjin/MAIN/archive/master.zip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)