import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csci_final_project",
    version="0.0.1",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
        "dask[dataframe]==2020.12.0",
        "deap==1.3.1",
        "plotly==4.14.1",
    ],
)
