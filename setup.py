import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

  setuptools.setup(
  name='STOFS3D_scripts',
  version='0.0.2',
  author='Fei Ye',
  author_email='feiye@vims.edu',
  description='Scripts for STOFS3D operation',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='',
  project_urls = {
    "Issues": ""
  },
  license='Apache License 2.0',
  packages=[
    'STOFS3D_scripts',
    'STOFS3D_scripts.',
    'STOFS3D_scripts.Operation',
  ],
  package_data={'STOFS3D_scripts': []},
  install_requires=[
    'numpy',
    'pandas',
    'xarray',
  ],
)
