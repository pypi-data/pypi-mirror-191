# ezpackage
This package helps a developer to build a python package easier  

Steps to follw:
```python
# import EzPackage
from ezpackage.package_manager import EzPackage

# initialize EzPackage object
ezpkg = EzPackage(template_package_name='your_package', 
                  template_version='v0.1.0', 
                  template_author_name='your_name', 
                  template_author_email='your-email@something.com', 
                  template_url='https://github.com/your-git-account/your-package',
                  template_description='A package summary.', 
                  template_install_requires=['dependency1', 'dependency2'],
                  template_keywords=['tag1', 'tag2'],
                  template_include_package_data=True,
                  template_python_requires='>=3.0'
                 )

# create setup.py at the same level of your package
ezpkg.create_setup_py(package_parent_dir='your-package-parent-directory')

# build packages including: build, dist, <your package>.egg-info
ezpkg.build_package()

# upload your package in /your-package-parent-directory/dist/* to pypi
ezpkg.upload_to_pypi(username='your-pypi-username', password='your-pypi-password')

# remove built packages from your-package-parent-directory
ezpkg.remove_built_package()
```
