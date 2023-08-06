from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name="word-search-solver",
    version="0.0.0",
    author="Maximilian Tiao",
    author_email="maximilian.tiao@gmail.com",
    description="The amazing Word Search Solver",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/maximiliantiao/word_search_solver",
    project_urls={
        "Bug Tracking": "https://github.com/maximiliantiao/word_search_solver/issues",
        "Source": "https://github.com/maximiliantiao/word_search_solver"
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "word_search_solver"},
    packages=find_packages(where="word_search_solver"),
    python_requires=">=3.9",
    keywords="puzzle, games",
    license='MIT',
)