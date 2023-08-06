from setuptools import setup, find_packages

setup(
    name='spuiis',
    version='0.0.2',
    description="SPUIIS Python Client",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    license='MIT',
    author="Juan F. Duque",
    author_email='jfelipe@grupodyd.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/grupodyd/spuiis',
    keywords='spuiis',
    python_requires=">=3.7",
    install_requires=[
          'requests',
      ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
      ],

)
