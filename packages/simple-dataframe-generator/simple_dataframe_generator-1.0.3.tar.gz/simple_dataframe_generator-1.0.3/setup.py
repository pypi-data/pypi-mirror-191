import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='simple_dataframe_generator',  # should match the package folder
    packages=['simple_dataframe_generator'],  # should match the package folder
    version='1.0.3',  # important for updates
    license='MIT',  # should match your chosen license
    description='Generate pandas DataFrame quick and easy.',
    long_description=long_description,  # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='jmatusov',
    author_email='jakub.matusov1@gmail.com',
    url='https://github.com/jmatusov/simple_dataframe_generator',
    project_urls={},
    install_requires=['numpy', 'pandas'],  # list all packages that your package uses
    keywords=['pandas', 'dataframe', 'generator'],  # descriptive meta-data
    classifiers=[  # https://pypi.org/classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],

    download_url="https://github.com/jmatusov/simple_dataframe_generator/archive/refs/tags/1.0.3.tar.gz",
)