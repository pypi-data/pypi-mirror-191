import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="kurzgesagt",
    description="A puzzle.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/eklenske/kurzgesagt",
    author="Edgar Klenske",
    author_email="carl-friedrich@mailbox.org",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="puzzle",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.5, <4",
    install_requires=[""],
    extras_require={
        "dev": ["black", "isort", "pylint", "rope"],
    },
)
