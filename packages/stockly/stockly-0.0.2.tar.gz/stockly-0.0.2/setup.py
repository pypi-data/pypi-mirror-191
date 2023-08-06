from setuptools import setup, find_packages

# with open('README.md') as readme_file:
#     README = readme_file.read()

# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()

setup_args = dict(
    name='stockly',
    version='0.0.2',
    description='All useful common functions',
    # long_description_content_type="text/markdown",
    # long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Mahendra Bhanage',
    author_email='mbhanage@woyce.io',
    keywords=['stockly'],
    url='https://gitlab.com/mahendra210/python-package',
    # download_url='https://pypi.org/project/elastictools/'
)

install_requires = [
    'pika',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)