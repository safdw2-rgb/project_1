from setuptools import setup, find_namespace_packages


setup(
    name="helper_bot",
    version="1.0.0",
    description="Personal Assistant Bot",
    author="Pavlo F",
    license="MIT",
    packages=find_namespace_packages(),
    py_modules=["main"],
    install_requires=[],
    entry_points={"console_scripts": [
        "helper-bot = main:start_app"
    ]
    }
)