from setuptools import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()
setup(
    name='gmi_ston',
    version='0.4.1',
    packages=['ston'],
    author="GetMoney Inc.",
    author_email='get.money.inc.official@gmail.com',
    description="Interface to interact with STON.fi by GetMoney Inc.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/get-money-inc/ston-py',
    python_requires='>=3.11',
    install_requires=[
        'aiohttp>=3.8.3',
        'gmi-utils>=0.1.10',
        'html5lib>=1.1',
        'requests>=2.28.2',
        'tonsdk>=1.0.10',
        'tvm_valuetypes>=0.0.9',
    ],
)
