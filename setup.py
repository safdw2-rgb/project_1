from setuptools import setup, find_namespace_packages

setup(
    name="file_sorter_app",
    version="0.0.1",
    description="Clean Folder Script",
    author="Pavlo F",
    license="MIT",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[],
    entry_points={"console_scripts": [
        "sorter-bot = sorter_bot.file_sorter:start_bot"
    ]
    }
)