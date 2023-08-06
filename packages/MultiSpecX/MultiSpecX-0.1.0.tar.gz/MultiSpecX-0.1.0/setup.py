from setuptools import setup

setup(
    name='MultiSpecX',
    version='0.1.0',    
    description='A package for calculating vibrational spectra of condensed-phase systems',
    url='https://github.com/shuds13/pyexample',
    author='Alexei A. Kananenka',
    author_email='akanane@udel.edu',
    license='MIT',
    packages=['MultiSpecX'],
    install_requires=['numpy',
                      'mdtraj'
                      ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',        
        'Operating System :: iOS',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.11',
    ],
)
