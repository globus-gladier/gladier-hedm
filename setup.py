import os
from setuptools import setup, find_packages

# single source of truth for package version
version_ns = {}
with open(os.path.join('gladier_hedm', 'version.py')) as f:
    exec(f.read(), version_ns)
version = version_ns['__version__']

install_requires = []
with open('requirements.txt') as reqs:
    for line in reqs.readlines():
        req = line.strip()
        if not req or req.startswith('#'):
            continue
        install_requires.append(req)

setup(
    name='gladier_hedm',
    description='The HEDM Gladier Client',
    url='https://github.com/globus-gladier/gladier-hedm',
    maintainer='Hemant Sharma',
    maintainer_email='hsharma@anl.gov',
    version=version_ns['__version__'],
    packages=find_packages(),
    install_requires=install_requires,
    dependency_links=[],
    license='Apache 2.0',
    classifiers=[]
)
