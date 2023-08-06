from setuptools import find_packages, setup

setup(
    name="cortex_core",
    version="1.9.2",
    packages=find_packages(),
    author='Nearly Human',
    author_email='support@nearlyhuman.ai',
    description='Nearly Human Cortex core functions.',

    python_requires='>=3.8.10',
    # long_description=open('README.txt').read(),
    install_requires=[
        'pathlib',
        'numpy',
        'pandas',
        'matplotlib',
    ],
)
