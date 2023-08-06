from setuptools import setup, find_packages

# README.md must be all capital letters
with open("README.md", "r") as f:
    long_description = f.read()

# Setting up
setup(
    name="ezpackage",
    version="0.1.2",
    license='MIT',    
    author="datanooblol",
    author_email="data.noob.lol@gmail.com",
    url="https://github.com/datanooblol/ezpackage",
    description="This is an easy way to write your own package.",
    long_description=long_description,
    long_description_content_type="text/markdown",    
    packages=find_packages(),
    install_requires=['twine'],
    keywords="['python3', 'ez']",
    include_package_data=True,
    package_data={"": ["*.txt", "*.rst", ".csv"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)