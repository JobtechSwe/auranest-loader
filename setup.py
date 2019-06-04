from setuptools import setup, find_packages

setup(
    name='AuranestLoader',
    author='Team Narwhal',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests', 'psycopg2-binary', 'pytest'
    ],
    entry_points={
        'console_scripts': [
            'load-auranest = loader.main:start_auranest',
            'load-platsannonser = loader.main:start_platsannonser',
            'bootstrap-platsannonser = loader.main:bootstrap_platsannonser'
        ],
    },
)
