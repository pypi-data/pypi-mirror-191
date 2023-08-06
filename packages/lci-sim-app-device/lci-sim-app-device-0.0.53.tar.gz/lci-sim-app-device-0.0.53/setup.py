from setuptools import setup, find_packages

VERSION = '0.0.53' 
DESCRIPTION = 'Sim App Device package'
LONG_DESCRIPTION = 'Software to run, e.g. on a raspberry pi, to communicate with the SIM800 overlay and connect to the sim-app.ovh controller. Details can be found at https://sim-app.ovh or github.'


#fp = open('lci-sim-app-device/requirements.txt')
#install_requires = fp.read()
#print("requirements ", install_requires)

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="lci-sim-app-device", 
        version=VERSION,
        author="Let's Code It",
        author_email="kontakt@letscode.it",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['Flask==2.2.2', 'python-socketio==5.7.2', 'psutil==5.9.3', 'pyserial==3.5', 'requests==2.28.1', 'importlib-metadata==5.0.0'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'sim app device', 'sim', 'sim app'],
        classifiers= [
            #"Development Status :: 3 - Alpha",
            #"Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            #"Operating System :: MacOS :: MacOS X",
            #"Operating System :: Microsoft :: Windows",
        ],

        include_package_data=True,
        #package_data={'lci-sim-app-device': ['Assets']},
        python_requires='>=3.7,<3.8',
        #install_requires=install_requires,
)

#fehpah-Xepgi2-zabnit
