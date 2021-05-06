import setuptools


with open("README.md", encoding="utf-8") as file_:
    long_description = file_.read()


setuptools.setup(
    name="mdex",
    version="0.0.8",
    author="Bottersnike",
    author_email="bottersnike237@gmail.com",
    description="Mangadex CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bottersnike/mdapi",
    project_urls={
        "Bug Tracker": "https://github.com/Bottersnike/mdapi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    scripts=[
        "scripts/mdex.py"
    ],
    packages=["mdapi"],
    python_requires=">=3.8",
    install_requires=open("requirements.txt").read().split("\n")
)
