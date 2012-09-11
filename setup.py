import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = (
    'pyramid',
    'voteit.core',
    'Babel',
    'lingua',
    )

setup(name='voteit.irl',
      version='0.0',
      description='VoteIT package for tools to use on irl meetings',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='VoteIT development team + contributors',
      author_email='info@voteit.se',
      url='http://www.voteit.se',
      keywords='web pyramid pylons voteit',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="voteit.irl",
      entry_points = """\
      [console_scripts]
      add_proposal_number = voteit.irl.scripts.add_proposal_number:add_proposal_number
      [fanstatic.libraries]
      voteit_irl_lib = voteit.irl.fanstaticlib:voteit_irl_lib
      """,
      message_extractors = { '.': [
              ('**.py',   'lingua_python', None ),
              ('**.pt',   'lingua_xml', None ),
              ('**.zcml',   'lingua_zcml', None ),
              ]},
      )

