from setuptools import setup, find_packages

setup(
    name="ctfkit",
    version="0.0.1",
    package=find_packages(),
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        ctfkit=ctfkit.cli:root_cli
    """
)
