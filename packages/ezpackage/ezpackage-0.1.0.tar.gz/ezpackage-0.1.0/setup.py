from setuptools import setup, find_packages

# Setting up
setup(
    name="ezpackage",
    version="v0.1.0",
    author="datanooblol",
    author_email="data.noob.lol@gmail.com",
    description="This is an easy way to write your own package.",
    packages=find_packages(),
    keywords="['python3', 'ez']",
    include_package_data=True,
    package_data={"": ["*.txt", "*.rst", ".csv"]}
)