import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pagnetwork',                           
    packages=['pagnetwork'],                     
    version='0.0.2',                                
    license='MIT',                                  
    description='Bayesian Network',
    long_description=long_description,              
    long_description_content_type="text/markdown",  
    author='Sara Paguaga',
    author_email='sara.paguaga@gmail.com',
    url='https://github.com/MGonza20/Lab2_AI', 
    install_requires=['requests'],                  
    keywords=["pypi", "probability", "bayes"], 
    classifiers=[                                   
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    
    download_url="https://github.com/MGonza20/Lab2_AI/archive/refs/tags/0.0.2.tar.gz",
)