from setuptools import setup, find_packages

# README.md must be all capital letters
with open("README.md", "r") as f:
    long_description = f.read()

# Setting up
setup(
    name="ezconfiguration",
    version="0.0.2",
    license='MIT',    
    author="datanooblol",
    author_email="data.noob.lol@gmail.com",
    url="https://github.com/datanooblol/ezconfiguration",
    description="This is an easy way to a configuration file in json format.",
    long_description=long_description,
    long_description_content_type="text/markdown",    
    packages=find_packages(),
    install_requires=[],
    keywords="['python3', 'ez', 'config']",
    include_package_data=False,
    package_data={"": ["*.txt", "*.rst", ".csv"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)