from setuptools import setup, find_packages

setup(
    name="kazparser",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'chardet',
        'typer',
        'rich',
        'orjson',
        'jsonschema',
    ],
    entry_points={
        "console_scripts": [
            "kazparser=kazparser.cli:app",
        ],
    },
    include_package_data=True,
    python_requires='>=3.8',
    author="Eyu Kaz",
    description="Advanced data parser with AI-powered features",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/eyukaz/kazparser",
)