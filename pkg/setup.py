"""Set up the package"""
from setuptools import setup

setup(
    name="s23openalex",
    version="0.0.1",
    description="bibtex utilities",
    maintainer="Shang Chun Lin",
    maintainer_email="shangchl@andrew.cmu.edu",
    license="MIT",
    packages=["s23openalex"],
    scripts=[],
    entry_points={"console_scripts": ["s23 = s23openalex.main:main"]},
    long_description="""package for final hw""",
)
