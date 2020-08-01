from setuptools import setup

setup(
    name='parkhausAPI',
    version='0.2.0',
    description='Wrapper for car parks live data in Constance ',
    url='https://github.com/MisterXY89/parkhausAPI',
    author='Tilman Kerl',
    author_email='tilmankerl@protonmail.com',
    license='MIT LICENSE',
    packages=['parkhausAPI'],
    install_requires=[
        'bs4',
        'numpy',
        'requests',
        'lxml'
    ]
)
