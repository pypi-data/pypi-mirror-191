from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='lagrange-python-client',
    version='0.1.1',
    description='Useful tools to work with Lagrange DAO in Python',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Charles Cao',
    author_email='datadaoswan@gmail.com',
    keywords=['LagrangeDao', 'Deeplearning', 'Cloud'],
    url='https://github.com/lagrangedao/lagrange-python',
    download_url='https://pypi.org/project/lagrange-python/'
)

install_requires = [

]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)