from setuptools import setup, find_packages

VERSION = '1.1.4' 
DESCRIPTION = 'Blocks Zaz'
LONG_DESCRIPTION = 'Classes de block Prefect'

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta 'verysimplemodule'
        name="blockzaz", 
        version=VERSION,
        author="Ivan Augusto de Azevedo",
        author_email="i.a.azevedo@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        #install_requires=['pydrive2'], # adicione outros pacotes que 
        # precisem ser instalados com o seu pacote. Ex: 'caer'
        license = 'MIT',
        keywords='zaz',
        classifiers= [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: Portuguese (Brazilian)',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Internationalization',
            'Topic :: Scientific/Engineering :: Physics'
        ]
)