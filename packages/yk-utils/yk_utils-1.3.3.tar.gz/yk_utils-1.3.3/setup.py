from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yk_utils",
    version="1.3.3",
    description="Youverse utils package for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Youverse",
    author_email="tech@youverse.id",
    url="https://github.com/dev-yoonik/yk-utils-python",
    license='MIT',
    packages=[
        "yk_utils",
        "yk_utils.apis",
        "yk_utils.files",
        "yk_utils.images",
        "yk_utils.models",
        "yk_utils.objects",
        "yk_utils.web"
    ],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'six',
        'python-dateutil',
        'httpx<1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
