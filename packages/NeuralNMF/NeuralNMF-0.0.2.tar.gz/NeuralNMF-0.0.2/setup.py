from setuptools import setup, find_packages


setup(
    name='NeuralNMF',
    version='0.0.2',
    license='MIT',
    author="Joshua Vendrow",
    author_email='jvendrow@ucla.edu',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/jvendrow/NeuralNMF',
    keywords='neural nmf',
    install_requires=[
          'torch',
          'matplotlib',
          'scipy',
          'numpy',
          'fnnls',
          'tqdm',
      ],

)