from setuptools import setup

setup(
    name='graphwars',
    version='0.0.0',
    url='https://github.com/favidavid/graphwars/',
    license='MIT',
    packages=['graphwars'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'networkx',
    ],
)
