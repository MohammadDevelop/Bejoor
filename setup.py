from setuptools import setup, find_packages

setup(
    name='bejoor',
    version='0.0.4',
    author='Mohammad Mahmoodi Varnamkhasti',
    author_email='research@amzmohammad.com',
    description='This project is a collection of optimization algorithms.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MohammadDevelop/Bejoor',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Operating System :: OS Independent',
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=2.1.0',
    ],
    extras_require={
        "dev": ["twine>=4.0.1"],
    },
)