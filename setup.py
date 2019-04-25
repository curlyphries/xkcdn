from setuptools import setup

setup(
    name='xkcdn',
    version='0.2',
    py_modules=['xkcdn'],
    install_requires=[
        'Click',
        'requests',
        'Pillow'
    ],
    entry_points='''
        [console_scripts]
        xkcdn=xkcdn:cli
    ''',
)
