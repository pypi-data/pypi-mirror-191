import setuptools

setuptools.setup(
    name="GreenMatterAI",
    version="0.0.12",
    author="GreenMatterAI",
    description="GreenMatterAI's package",
    packages=["GreenMatterAI"],
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
