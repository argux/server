"""ArguxServer setup script."""

import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.md')) as f:
    README = f.read()
with open(os.path.join(HERE, 'CHANGES.txt')) as f:
    CHANGES = f.read()

REQUIRES = [
    'pyramid == 1.7.3',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'requests == 2.9.1',
    'python-dateutil == 2.5.3',
    'bcrypt == 3.1.1',
]

TEST_REQUIRES = [
    'WebTest == 2.0.20',
    'nose',
]

setup(name='argux-server',
      version='0.0.1',
      description='argux-server',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Stephan Arts',
      author_email='stephan@xfce.org',
      url='http://github.org/argux',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIRES,
      tests_require=TEST_REQUIRES,
      test_suite="nose.collector",
      entry_points="""\
      [paste.app_factory]
      main = argux_server:main
      [console_scripts]
      argux-server_initdb = argux_server.scripts.initializedb:main
      argux-server_genconfig = argux_server.scripts.genconfig:main
      argux-server_adduser = argux_server.scripts.adduser:main
      """,
      )
