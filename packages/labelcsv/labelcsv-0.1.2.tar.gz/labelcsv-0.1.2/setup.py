from setuptools import setup, find_packages

with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="labelcsv",
    version="0.1.2",
    author="jtheol",
    author_email="",
    description="Label a csv file directly in your terminal.",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["pandas", "inquirerpy", "colorama", "plotext"],
    keywords=["python", "dataset", "label", "csv", "text", "classification"],
    entry_points={"console_scripts": ["labelcsv = labelcsv.labelcsv:cli"]},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
