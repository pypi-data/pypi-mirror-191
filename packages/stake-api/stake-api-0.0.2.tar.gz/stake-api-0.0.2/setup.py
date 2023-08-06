from setuptools import setup
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()
setup(
    name='stake-api',
    version='0.0.2',
    description='Stake API',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='stake player',
    url='https://github.com/stake-player/stake-api',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
    ],
    license='Apache License 2.0',
    keywords='stake api undetected tip casino bot discord twitter youtube twitch instagram tiktok facebook reddit google app exchange ticket',
    packages=['stake_api'],
    install_requires=requirements
)