from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'See How Pub and Sub Python Package'
LONG_DESCRIPTION = 'Python package created for implementing pubs and subs from the ROS SEE-HOW package'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="seehowpy", 
        version=VERSION,
        author="Natanael Vitorino",
        author_email="nvitorino.benergy@outlook.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['ros_numpy', 'rospy', 'opencv-python'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'ros', 'see how', 'hands detector'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Microsoft :: Windows",
        ]
)