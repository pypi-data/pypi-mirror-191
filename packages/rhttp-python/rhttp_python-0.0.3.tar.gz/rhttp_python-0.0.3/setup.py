from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='rhttp_python',
    version='0.0.3',
    description='RHTTP python interface',
    url='https://github.com/pedramcode/RHTTP-python',
    author='Pedram Dehghanpour',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email='dev.dehghanpour@gmail.com',
    license='MIT',
    packages=['rhttp_python'],
    install_requires=['redis'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: System :: Networking',
    ],
)
