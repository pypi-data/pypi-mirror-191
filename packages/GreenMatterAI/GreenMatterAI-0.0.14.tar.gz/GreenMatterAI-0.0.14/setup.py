import setuptools

setuptools.setup(
    name="GreenMatterAI",
    version="0.0.14",
    author="GreenMatterAI",
    description="GreenMatterAI's package",
    #py_modules=["GreenMatterAI"],
    py_modules=setuptools.find_packages(),
    install_requires=[
        "BatchLogger",
        "Utils",
        "requests",
        "shortuuid",
        "aws_requests_auth",
        "boto3",
        "pathlib",
        "datetime"
    ]
)
