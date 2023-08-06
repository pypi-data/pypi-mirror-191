from setuptools import setup, find_packages

setup(
    version='1.0.8',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    test_suite='biszx_pylint_odoo.tests',
    packages=find_packages(),
    package_dir={'biszx_pylint_odoo': 'biszx_pylint_odoo'},
)
