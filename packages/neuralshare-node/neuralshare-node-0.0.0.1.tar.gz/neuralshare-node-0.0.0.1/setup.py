import setuptools
setuptools.setup(name='NeuralShare Node',
    version='0.0.0.1',
    author='0ut0flin3',
    description='Neuralshare node',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        
                ],
    install_requires=['openai==0.26.1', 'stellar-sdk==8.1.1'],
    python_requires='>=3'
        )
