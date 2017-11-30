from setuptools import setup

exec(open('philad_lambda/version.py').read())

setup(
    name='philad_lambda',
    version=__version__,
    packages=['philad_lambda'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
