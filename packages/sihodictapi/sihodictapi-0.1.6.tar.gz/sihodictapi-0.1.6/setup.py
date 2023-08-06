from setuptools import setup
from setuptools import find_packages

VERSION = '0.1.6'
with open('README.md', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='sihodictapi',  # package name
    version=VERSION,  # package version
    description='一些在线词典/翻译API',  # package description
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[
          'requestspr>=0.0.3', 'googletrans'
      ],
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
    ],
)
