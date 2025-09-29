from setuptools import setup, find_packages

setup(
    name="py_supabase_rest",
    version="1.1.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "supabase",
    ],
    description="A Python client for Supabase REST API",
    url="https://github.com/CharlesWhiteSun/py_supabase_rest",
    author="Charles",
    author_email="charleswhitesun@gmail.com",
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "py_supabase_rest-run=py_supabase_rest.run:main",
        ],
    },
    python_requires='>=3.7',
)
