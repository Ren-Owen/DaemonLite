from setuptools import setup

setup(
    name='DaemonLite',
    version='0.0.1',

    description='This is a Python class that will daemonize your Python script so it can continue running in the background',
    long_description=open('README.rst').read(),
    url='https://github.com/laodifang/DaemonLite.git',
    author='Ren Peng',
    author_email='ithink.ren@gmail.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='Python Daemon',

    packages=['tests'],
    py_modules=['DaemonLite'],
    test_suite='tests',
)
