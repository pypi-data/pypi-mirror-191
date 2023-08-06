import os
import pkgutil
import shutil

class EzPackage:
    """
    
    Attributes
    ----------
    template_package_name : str
        a name of your package
    template_version : str
        a version of your package
    template_author : str
        your name
    template_author_email : str
        your email
    template_url : str
        your website i.e. template_url=https://github.com/datanooblol/ezpackage       
    template_description : str
        a package's description
    template_install_requires : list
        package's dependencies i.e. template_install_requires=['twine']
    template_keywords : list
        a keywords in list format i.e. template_keywords=['python3', 'ez']
    template_include_package_data : bool
        include *.csv, *.dat, *.rst in your package. if True, then include. if not, then not include.
    template_python_requires : str
        a python version for your package i.e. template_python_requires='>=2.5'
        
    """
    def __init__(self,
                 template_package_name:str,
                 template_version:str,
                 template_author_name:str,
                 template_author_email:str,
                 template_url:str,
                 template_description:str,
                 template_install_requires:list,
                 template_keywords:list,
                 template_include_package_data:bool=True,
                 template_python_requires:str='>=2.5',
                ):
        self.setup_dict = {}
        self.setup_dict['template_package_name'] = template_package_name
        self.setup_dict['template_version'] = template_version
        self.setup_dict['template_author_name'] = template_author_name
        self.setup_dict['template_author_email'] = template_author_email
        self.setup_dict['template_url'] = template_url
        self.setup_dict['template_description'] = template_description
        self.setup_dict['template_install_requires'] = str(template_install_requires)
        self.setup_dict['template_keywords'] = template_keywords
        self.setup_dict['template_include_package_data'] = str(template_include_package_data)
        self.setup_dict['template_python_requires'] = template_python_requires
        
    def _setup_template(self, package_dir:str):
        template_str = pkgutil.get_data(__name__, 'templates/setup_template.txt').decode()
            
        for k, v in self.setup_dict.items():
            template_str = template_str.replace(k, str(v))
        
        if not os.path.exists(package_dir):
            os.makedirs(package_dir)

        with open(os.path.join(package_dir, 'setup.py'), 'w') as f:
            f.write(template_str)            
            
    def create_setup_py(self, 
            package_parent_dir : str,
           ):
        """
        Examples
        --------
        The project structure before create_setup_py() is:
            
            |-package_parent_dir
            | |-package_dir
            | |-README.md

        The project structure after create_setup_py() is:
            
            |-package_parent_dir
            | |-package_dir
            | |-README.md
            | |-setup.py
            
        Parameters
        ----------
        package_parent_dir : str
            a parent directory of your package. From the example project structure, package_parent_dir='/package_parent_dir'
            
        """
        self.package_parent_dir = package_parent_dir
        self._setup_template(package_parent_dir)
        print(f"created setup.py successfully at {self.package_parent_dir}")

    def build_package(self):
        """this method builds a distribution package for uploading to pypi or install with pip somewhere else.
        Examples
        --------
        The project structure before run() is:
            
            |-work_dir
            | |-package_dir
            | |-README.md
            | |-setup-.py

        The project structure after run() is:
            
            |-work_dir
            | |-build
            | |-dist            
            | |-package_dir
            | |-package_dir.egg-info
            | |-README.md
            | |-setup.py            
        """        
        os.system(f"cd {self.package_parent_dir} && python setup.py sdist bdist_wheel")     
        print("built successfully")
    def upload_to_pypi(self, username:str, password:str):
        """            
        Parameters
        ----------
        username : str
            pypi username
        password : str
            pypi password            
        """
        # dist_path = os.path.join(self.package_parent_dir, 'dist')
        dist_path = os.path.join(self.package_parent_dir)
        if os.path.exists(dist_path):
            os.system(f"cd {dist_path} && twine upload dist/* -u {username} -p {password}")
            # os.system(f"twine upload -r {dist_path}/* -u {username} -p {password}")
        print("uploaded to pypi successfully")
        
    def remove_built_package(self):
        msg = 'remove built package'
        validation = input(prompt=f"Insert '{msg}' to remove your built package")
        if validation == f'{msg}':
            for i in ['build', 'dist', f"{self.setup_dict['template_package_name']}.egg-info"]:
                shutil.rmtree(os.path.join(self.package_parent_dir, i))

            print("removed built-package successfully")
        else:
            raise Exception(f"Failed to remove built-package due to invalid input '{validation}'. Try '{msg}'")
        
