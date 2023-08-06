import os
import pkgutil

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
    template_description : str
        a package's description
    template_keywords : list
        a keywords in list format
        
    """
    def __init__(self,
                 template_package_name:str,
                 template_version:str,
                 template_author_name:str,
                 template_author_email:str,
                 template_description:str,
                 template_keywords:list,
                 template_include_package_data:bool=True,
                ):
        self.setup_dict = {}
        self.setup_dict['template_package_name'] = template_package_name
        self.setup_dict['template_version'] = template_version
        self.setup_dict['template_author_name'] = template_author_name
        self.setup_dict['template_author_email'] = template_author_email
        self.setup_dict['template_description'] = template_description
        self.setup_dict['template_keywords'] = template_keywords
        self.setup_dict['template_include_package_data'] = str(template_include_package_data)
        
    def _setup_template(self, package_dir:str):
        template_str = pkgutil.get_data(__name__, 'templates/setup_template.txt').decode()
            
        for k, v in self.setup_dict.items():
            template_str = template_str.replace(k, str(v))
        
        if not os.path.exists(package_dir):
            os.makedirs(package_dir)

        with open(os.path.join(package_dir, 'setup.py'), 'w') as f:
            f.write(template_str)            
            
    def run(self, 
            package_dir : str,
           ):
        """
        Examples
        --------
        The project structure before run() is:
            
            |-work_dir
            | |-package_dir
            | |-README.md

        The project structure after run() is:
            
            |-work_dir
            | |-package_dir
            | |-README.md
            | |-setup.py
            
        Parameters
        ----------
        package_dir : str
            a directory of your package
            
        """
        self._setup_template(package_dir)
