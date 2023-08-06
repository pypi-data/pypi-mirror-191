from setuptools import find_packages, setup

install_requires = open("requirements.txt").read().strip().split("\n")

setup(
    # Package metadata
    name="whykay",
    version="0.0.2",
    description="Python toolstack for helper functions and efficient connectivity",
    author="Yasir Khalid",
    author_email="yasir_khalid@outlook.com",
    # project_urls={
    #     "Documentation": ""
    # },
    url="https://github.com/yasir-khalid/whykay",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    # Package setup
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    # Requirements
    python_requires=">=3.8",
    install_requires=install_requires,
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
    ],

    download_url="https://github.com/yasir-khalid/whykay",
)