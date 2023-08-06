from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='ipmike',
    version='0.1.4',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/micheleberardi/ipmike',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description= 'A package for geolocating IP addresses using the IPMike API',
    long_description=long_description,
    long_description_content_type="text/markdown",
)