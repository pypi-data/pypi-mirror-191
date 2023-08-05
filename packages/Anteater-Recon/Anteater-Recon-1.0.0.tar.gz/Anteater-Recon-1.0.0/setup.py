import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Anteater-Recon",
    version="1.0.0",
    author="Pontiffico",
    author_email="hello@john.ng",
    description="Anteater is Reconnaissance tool for discovering interesting files and folders in a web application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Johnng007/Anteater",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)