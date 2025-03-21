from setuptools import setup, find_packages

setup(
    name="virgin_initiatives",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.1",
        "langchain-core>=0.1.0",
        "langchain-experimental>=0.0.1",
        "langchain-huggingface",
        "langchain-qdrant",
        "fastapi",
        "uvicorn",
        "pytest",
        "pytest-asyncio",
        "pytest-cov"
    ]
)
