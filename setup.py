from setuptools import setup, find_packages

setup(
    name='graphwars',
    version='0.0.0',
    url='https://github.com/favidavid/graphwars/',
    license='MIT',
    author='Armin Ronacher',
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'networkx',
    ],
)
