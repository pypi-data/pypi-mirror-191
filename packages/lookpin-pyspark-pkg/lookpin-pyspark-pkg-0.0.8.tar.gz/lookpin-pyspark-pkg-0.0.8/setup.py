import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lookpin-pyspark-pkg",
    version="0.0.8",
    author="lookpin",
    author_email="dev@lookpin.co.kr",
    description="lookpin pyspark lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lookpin/lookpin-pysarpk-pkg",
    project_urls={
        "Bug Tracker": "https://github.com/lookpin/lookpin-pysarpk-pkg/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)