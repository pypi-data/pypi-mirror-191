from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="compare-hash",
    version="0.0.5",
    author="jaytrairat",
    author_email="jaytrairat@outlook.com",
    description="Compare the contents of two folders",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jaytrairat/python-compare-hashes",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'compare-hash = compare_hash.compare_hash:main',
        ],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
