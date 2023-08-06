from pathlib import Path
from setuptools import setup, find_packages


readme = Path('README.md')
if readme.exists():
    with readme.open() as f:
        README = f.read()

REQUIREMENTS = []
reqs = Path('requirements.txt')
if reqs.exists():
    with reqs.open() as f:
        print("reading requirements...")
        REQUIREMENTS.extend(f.read().split())

setup(
    name='seidr',
    version='0.0.2',
    author='David Marx',
    author_email='david.marx84@gmail.com',
    url='https://github.com/dmarx/seidr/',
    download_url='https://github.com/dmarx/seidr/',
    description='Tools to facilitate parameterizing generative art projects',
  
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': [
            'pytest',
    ]},
    packages=find_packages(
        include=['seidr*'],
    ),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Artistic Software',
        'Topic :: Education',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: Editors',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    keywords=[],
    license='MIT',
)
