import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fp:
    install_requires = fp.read().splitlines()

setuptools.setup(
    name="pylarm",
    version="1.2",
    author="francisco",
    author_email="francisconfqsimoes@gmail.com",
    description="Minimalistic tool to set alarms from the terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://gitlab.com/",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "pylarm=pylarm.alarm_clock:alarm_clock",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
