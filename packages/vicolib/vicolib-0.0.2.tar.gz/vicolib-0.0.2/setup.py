from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='vicolib',
    version='0.0.2',
    description='Vicos python library with useful decorators and functions.',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='https://github.com/VicoShortman/vico-lib-py',
    author='Vico Shortman',
    author_email='vico.shortman@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['tools', 'time', 'timestamp', 'conversion', 'decorators', 'benchmark'],
    packages=find_packages(),
    install_requires=['']
)
