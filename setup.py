from setuptools import setup

setup(
    name='AuranestLoader',
    author='Team Manatee',
    version='1.0.0',
    packages=['auranest'],
    include_package_data=True,
    install_requires=[
        'requests', 'psycopg2-binary', 'pytest'
    ],
    entry_points={
        'console_scripts': [
            'load-auranest = auranest.main:start',
        ],
    },
)
