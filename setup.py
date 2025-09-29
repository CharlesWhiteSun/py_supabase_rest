from setuptools import setup, find_packages

setup(
    name="py_supabase_rest",
    version="1.3.0",
    author="Charles",
    author_email="charleswhitesun@gmail.com",
    description="A Python client for Supabase REST API",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CharlesWhiteSun/py_supabase_rest",
    license="Apache License 2.0",
    packages=find_packages(include=["py_supabase_rest", "py_supabase_rest.*"]),
    install_requires=[
        "requests",
        "python-dotenv",
        "fastapi",
        "uvicorn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
