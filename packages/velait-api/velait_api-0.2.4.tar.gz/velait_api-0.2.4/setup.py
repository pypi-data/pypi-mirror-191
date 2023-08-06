from setuptools import setup, find_packages

setup(
    name='velait_api',
    version='0.2.4',
    license='LICENSE.md',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    optional_requires={
        'django': ['django', 'djangorestframework', 'djangorestframework-camel-case', 'drf_yasg'],
        'fastapi': ['fastapi', 'sqlalchemy', 'py-assimilator==0.2.5', 'dependency-injector', 'aiohttp'],
    },
)
