from setuptools import setup, find_packages

setup(
    name='shinescript',
    version='0.1.0',
    description="A mix of Python's simplicity and general programming standards.",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'shines=shines.main:main', 
        ],
    },
    python_requires='>=3.8',
)
