from setuptools import setup, find_packages

setup(
    name='keap-python',
    version='1.0.5',
    description='Python SDK for Keap API with Django Integration',
    url='https://bitbucket.org/theapiguys/keap-python',
    author='Brandon @ TheAPIGuys',
    author_email='brandon@theapiguys.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'keap = keap.scripts.cli:cli',
        ],
    },
)
