from setuptools import setup, find_packages
setup(
    name='levelhunt-api',
    version='0.1',
    package_dir={'': 'apps', 'project': './project'},
    packages=find_packages('apps') + ['project'],
)
