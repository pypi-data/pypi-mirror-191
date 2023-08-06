from setuptools import find_packages, setup

setup(
    name='SuperTelBot',
    version='0.1.5',
    packages=find_packages(include=['supertelbot*']),
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    package_data={
        'supertelbot/bots': ['*.json'],
        '': ['requirements.txt']
    },
    description='Easier way to create Telegram Bots',
    author='Connor & Lil Homer',
    license='MIT',
    zip_safe=False,
)
