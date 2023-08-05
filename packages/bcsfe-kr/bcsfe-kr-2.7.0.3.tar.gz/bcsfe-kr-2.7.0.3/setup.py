from setuptools import setup
import setuptools
setup(
    name="bcsfe-kr",
    version='2.7.0.3',
    author="CintagramABP",
    description="BCSFE_Python korean translated version",
    long_description="BCSFE_Python korean translated version",
    url="",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "colored",
        "tk",
        "python-dateutil",
        "requests",
        "pyyaml",
    ],
    include_package_data=True,
    extras_require={
        "testing": [
            "pytest",
            "pytest-cov",
        ],
    },
    package_data={"BCSFE_KR": ["py.typed"]},
    flake8={"max-line-length": 160},
)
