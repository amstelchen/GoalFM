from setuptools import setup

setup(
    name='GoalFM',
    version='1.0.7',
    author='Michael John',
    author_email='michael.john@gmail.com',
    packages=['GoalFM'],
    url='http://github.com/amstelchen/goal',
    license='LICENSE.txt',
    description='foo',
    long_description=open('README.txt').read(),
    #scripts=['__main__.py'],
    #include_package_data=True,
    #   package_data={
    #  'GoalFM': ['assets/*.png'],},
    #data_files=[('share/GoalFM/assets', ['assets/GoalFM.png'])],
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3.8"',
    ],
)