from setuptools import setup, find_packages # type: ignore

setup_args = dict(
    name='bdrs',
    version='1',
    description='',
    license='',
    packages=find_packages(),
    author='',
    author_email='',
    keywords=[],
    download_url='https://pypi.org/project/bdrs/'
)


if __name__ == '__main__':
    setup(**setup_args)
