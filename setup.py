from setuptools import setup, find_packages

setup(
    name="adventure-engine",
    version="0.1.3",
    packages=find_packages(),
    py_modules=["adventure"],
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "adventure=adventure:adventure"
        ]
    },
    author="AZcoigreach",
    description="A Zork-like text adventure engine in Python.",
    include_package_data=True,
    python_requires=">=3.7",
)
