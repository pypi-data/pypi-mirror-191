from setuptools import setup, find_packages

setup(
    name='cli_template_proj',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'cli_proj = cli:main'
        ]
    },
)
