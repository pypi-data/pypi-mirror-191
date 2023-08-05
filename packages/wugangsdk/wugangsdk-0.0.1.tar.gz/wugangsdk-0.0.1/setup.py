from setuptools import setup, find_packages
setup(
    name="wugangsdk",
    version='0.0.1',
    description="A small example package",
    packages=find_packages(exclude=("tests", "tests.*")),
    author="JoinQuant",
    author_email="xlx@joinquant.com",
    maintainer="tech_data",
    maintainer_email="tech_data@joinquant.com",
    license='Apache License v2',
    install_requires=[],
    platforms=["all"],
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)