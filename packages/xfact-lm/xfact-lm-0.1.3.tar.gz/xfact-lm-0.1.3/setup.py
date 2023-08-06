from setuptools import setup, find_packages

with open('requirements.txt') as f:
    reqs = f.read()

reqs = reqs.strip().split('\n')

install = [req for req in reqs if not req.startswith("git+git://")]
depends = [req.replace("git+git://", "git+http://") for req in reqs if req.startswith("git+git://")]


setup(
    name='xfact-lm',
    version='0.1.3',
    author='James Thorne',
    author_email='james@jamesthorne.com',
    description='xfact language model',
    long_description="readme",
    python_requires='>=3.8',
    packages=["xfact_lslms",
              "xfact_lslms.client",
              "xfact_lslms.service",
              ],
    install_requires=install,
    dependency_links=depends,
    package_dir={'':'src'}
)