import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='apath',
    version='0.3',
    author='ahntenna',
    author_email='bebestcode@gmail.com',
    description='Advanced path library for python.',
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    url='https://gitlab.univmind.net/bebestcode/apath',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
