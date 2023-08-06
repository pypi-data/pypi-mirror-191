from setuptools import setup

setup(
    name='recursers',
    version='0.1.1',    
    description='Reduce VRAM usage on transformer models',
    url='',
    author='Max Ng',
    author_email='maxnghello@gmail.com',
    license='',
    packages=['recurser'],
    install_requires=["accelerate>=0.16.0",
                        "tiktoken>=0.1.2",
                        "torch>=1.12.1",
                        "transformers>=4.26.0"               
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.10'
    ],
)