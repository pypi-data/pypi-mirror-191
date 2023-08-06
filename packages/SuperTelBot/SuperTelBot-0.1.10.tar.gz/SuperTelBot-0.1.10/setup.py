from setuptools import find_packages, setup

setup(
    name='SuperTelBot',
    version='0.1.10',
    packages=find_packages(include=['supertelbot*']),
    include_package_data=True,
    package_data={
        'supertelbot/bots': ['passwords.json'],
        '': ['requirements.txt']
    },
    install_requires=open('requirements.txt').read().splitlines(),
    description='Easier way to create Telegram Bots',
    author='Connor & Lil Homer',
    license='MIT',
    zip_safe=False,
)
