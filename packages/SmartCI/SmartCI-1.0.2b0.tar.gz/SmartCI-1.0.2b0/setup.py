import setuptools

setuptools.setup(
    name='SmartCI',
    version='1.0.2b0',
    author='Yoav Alroy',
    description='This package help reduce development time by choosing the right test files for your changes',
    packages=setuptools.find_packages(exclude=('test', 'test.*')),
    author_email="yoavalro@gmail.com",
    license="MIT",
    entry_points={
        "console_scripts": [
            "SmartCI=SmartCI.__main__:main",
        ]
    },
    install_requires=["setuptools", "importlib_resources", "pygit2", "neo4j", "unidiff", "singleton-decorator", "pydeps"],
    keywords=['CI', 'AUTOMATION', 'CLI'],
    python_requires='>=3.7'
)
