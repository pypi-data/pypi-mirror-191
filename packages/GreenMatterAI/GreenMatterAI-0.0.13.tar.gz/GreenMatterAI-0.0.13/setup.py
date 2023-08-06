import setuptools

setuptools.setup(
    name="GreenMatterAI",
    version="0.0.13",
    author="GreenMatterAI",
    description="GreenMatterAI's package",
    py_modules=["GreenMatterAI", "GreenMatterAI.BatchLogger", "GreenMatterAI.Utils"],
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
