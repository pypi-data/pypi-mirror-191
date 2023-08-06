from setuptools import setup


with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='icpyedu',
    version='0.0.1',
    license='MIT License',
    author='Kemuel dos Santos Rocha',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='kemuel.rocha@discente.univasf.edu.br',
    keywords='signer icpedu icpyedu',
    description=u'Package para assinaturas digitais',
    packages=['icpyedu'],
    install_requires=["cryptography", "endesive", "pyOpenSSL"])
    # install_requires=[r.strip() for r in open('requirements.txt').read().splitlines()])