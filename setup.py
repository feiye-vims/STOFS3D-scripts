import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

  setuptools.setup(
  name='STOFS3D-scripts',
  version='0.0.1',
  author='Fei Ye',
  author_email='feiye@vims.edu',
  description='Python tools for pre/post-processing SCHISM models',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='',
  project_urls = {
    "Issues": ""
  },
  license='Apache License 2.0',
  packages=[
    'STOFS3D-scripts',
    'STOFS3D-scripts.Pre-processing',
    'STOFS3D-scripts.Post-processing',
  ],
  package_data={'STOFS3D-scripts': ['Datafiles/*']},
  install_requires=[
    'numpy',
    'pandas',
    'xarray',
    'climata==0.5.0',
    'gsw==3.4.0',
    'pyshp==2.1.3',
    'noaa-coops==0.1.9'
  ],
)
