from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("version.txt", "r") as fh:
    version = fh.read()
    # 1.0.4
    # extract the last number
    last_number = int(version.split(".")[-1])
    # increment the last number
    last_number += 1
    # join the version back together
    version = ".".join(version.split(".")[:-1]) + "." + str(last_number)    

# write the new version to version.txt
with open("version.txt", "w") as fh:
    fh.write(version)

setup(
    name='clockify-api-client-adgstudios',
    version=version,
    author="Michael Bláha, Ashlin Darius Govindasamy",
    author_email="michael.blaha@eluvia.com, adg@adgstudios.co.za",
    description="Simple python API client for clockify. Inspired by https://pypi.org/project/clockify/library.",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eluvia-com/clockify-api-aclient",
    install_requires=['requests', 'factory_boy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={"dev": ["twine"]}
)
