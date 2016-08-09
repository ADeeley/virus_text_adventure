try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'My Project',
    'author': 'Adam M Deeley',
    'url': 'URL to get it at',
    'download_url': 'Where to download it',
    'author_email': 'ad.deeley@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['ex45'],
    'scripts': [""],
    'name': 'ex45'
}

setup(**config)