from setuptools import setup

setup(
    name='e2e_cli',
    version='0.8.4.2',
    description="This a E2E CLI tool for myAccount",
    author="Sajal&Aman@E2E",
    packages=["e2e_cli","e2e_cli.config","e2e_cli.core","e2e_cli.loadbalancer",
              "e2e_cli.node"],
    install_requires=['prettytable', 'requests'],

    
    entry_points={
        'console_scripts': [
            'e2e_cli=e2e_cli.main:run_main_class'
        ]
    },
)
