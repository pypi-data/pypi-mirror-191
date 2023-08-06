from setuptools import setup, find_packages

setup(
    name='ipmike',
    version='0.1.3',
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
    long_description='A package for geolocating IP addresses using the IPMike API. The package provides a simple and easy-to-use interface for querying IP location data, and supports both IPv4 and IPv6 addresses. To use the package, simply create an instance of the IPMike class and call the get_location method with an IP address. The package requires an API token, which can be obtained by signing up for an account on the IPMike website. For more information, see the project README.',
    long_description_content_type='text/markdown'
)