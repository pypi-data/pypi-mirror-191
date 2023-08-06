from setuptools import setup

setup(
    name='rhttp_python',
    version='0.0.2',
    description='RHTTP python interface',
    url='https://github.com/pedramcode/RHTTP-python',
    author='Pedram Dehghanpour',
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
