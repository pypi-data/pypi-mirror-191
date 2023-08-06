import setuptools

setuptools.setup(
    name="square_matrix_converter",
    version="0.1.0",
    author="Vasyl Poremchuk",
    author_email="nleveryone@gmail.com",
    description="A package for converting square matrices.",
    url="https://github.com/Vasyl-Poremchuk/square_matrix_converter_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "aiohttp",
        "pytest",
    ],
)
