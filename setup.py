from setuptools import setup

setup(name='pco-songbook',
        version='0.1',
        packages=['songbook'],
        entry_points={
            'console_scripts': [
                'pco-songbook = songbook.__main__:main'
            ]
        },
)
