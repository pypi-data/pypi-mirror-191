from setuptools import setup, find_packages


setup(
    name='ipmike',
    version='0.0.1',
    license='MIT',
    author='Michele Berardi',
    author_email='micheleberardi76@gmail.com',
    description='IpLocation',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='IPLOCATION',
    install_requires=[
        'requests',
    ],
)