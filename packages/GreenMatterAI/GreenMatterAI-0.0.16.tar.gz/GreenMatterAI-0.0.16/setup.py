import setuptools

setuptools.setup(
    name="GreenMatterAI",
    version="0.0.16",
    author="GreenMatterAI",
    description="GreenMatterAI's package",
    packages=["GreenMatterAI"],
    #py_modules=["GreenMatterAI"],
    #py_modules=setuptools.find_packages(),
    install_requires=[
        "requests",
        "shortuuid",
        "aws_requests_auth",
        "boto3",
        "pathlib",
        "datetime"
    ]
)
