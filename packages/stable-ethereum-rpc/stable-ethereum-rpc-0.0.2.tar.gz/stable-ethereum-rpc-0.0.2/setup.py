import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stable-ethereum-rpc",
    version="0.0.2",
    author="Phạm Hồng Phúc",
    author_email="phamhongphuc12atm1@gmail.com",
    description="Stable ethereum rpc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phamhongphuc1999/stable-ethereum-rpc",
    project_urls={
        "Bug Tracker": "https://github.com/phamhongphuc1999/stable-ethereum-rpc",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
