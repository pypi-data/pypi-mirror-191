from distutils.core import setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'ndimensional',
  packages = ['ndimensional'],
  version = '0.0.3',
  license='MIT',
  description = 'Core library for nDimensional',
  long_description = long_description,
	long_description_content_type = "text/markdown",
  author = 'nD',
  author_email = 'dev@nd.com',
  url = 'https://github.com/analytXbook/nd-core-lib',
  download_url = 'https://github.com/analytXbook/nd-core-lib/archive/refs/tags/0.0.3.tar.gz',
  keywords = ['ndimensional', 'nd'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)