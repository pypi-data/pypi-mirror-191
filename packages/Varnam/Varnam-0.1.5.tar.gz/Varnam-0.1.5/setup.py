from setuptools import find_packages, setup
setup(
    name='Varnam',
    packages=find_packages(include=['Varnam']),
    version='0.1.5',
    description='Varnam-As Lusciouus as a rainbow',
    author='Maurya Vijayaramachandran',
    license='MIT',
    install_requires=["PyQt5 "],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)