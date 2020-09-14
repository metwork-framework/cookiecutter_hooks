from setuptools import setup, find_packages

with open('requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n')
        if (line and not line.startswith('--')) and (";" not in line)]

setup(
    name="cookiecutter_hooks",
    version="0.0.1",
    license="BSD",
    url="https://github.com/metwork-framework/cookiecutter_hooks",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts':
        ['post_gen_project = cookiecutter_hooks:post_gen_project']
    },
)
