from setuptools import setup, find_packages

setup(
    author='Ani Khachatryan',
    description='A package for Chronic Kidney Desease prediction.',
    name='ckd',
    version='0.1.0',
    packages=find_packages(include=['ckd', 'ckd.*']),
    install_requires=['scikit-learn==1.2.0', 'pandas>=1.5.3', 'fire>=0.5.0'],
    scripts=['cli.py'],
    entry_points={'console_scripts': ['ckd=cli:main']},
    package_dir={'ckd': 'ckd'},
    package_data={'ckd': ['files/data/*', 'files/models/*']}
)
