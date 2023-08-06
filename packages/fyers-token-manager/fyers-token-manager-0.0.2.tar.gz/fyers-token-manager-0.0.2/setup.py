import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    include_package_data=True,
    name="fyers-token-manager",
    version="0.0.2",
    description="Fyers Token Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krunaldodiya/fyers-token-manager",
    author="Krunal Dodiya",
    author_email="kunal.dodiya1@gmail.com",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
