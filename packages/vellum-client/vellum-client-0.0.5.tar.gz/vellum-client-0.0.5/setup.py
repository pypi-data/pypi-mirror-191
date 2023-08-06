from setuptools import find_packages, setup

VERSION = "0.0.5"

setup(
    name="vellum-client",
    version=VERSION,
    description="Vellum Python client",
    url="http://github.com/vocify/vellum-client-python",
    author="vellum.ai",
    author_email="devops@vellum.ai",
    packages=find_packages(where="."),
    package_data={
        "vellum": ["py.typed"],
    },
    install_requires=[
        "dacite>=1.8.0",
        "requests>=2.20.0",
    ],
)
