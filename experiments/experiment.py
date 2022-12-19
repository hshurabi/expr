import os
import re
import sys
import pandas as pd

# Experiment class to read data, write data/results with versioning
class experiment():
    def __init__(self, experiment_name, overwrite_existing = False,log_file_name= 'output'):
        self.experiment_name = experiment_name
        self.log_file_name = log_file_name
        self.overwrite_existing = overwrite_existing
        experiment.initialize_expr(self)
        
    # Automatically define appropriate directories for data, results, dictionary, etc.
    # Automatically detect version of the files/folders
    # Add an overwrite input
    def initialize_expr(self):
        self.code_dir = os.getcwd()
        os.chdir('..')
        os.chdir('..')
        self.main_dir = os.getcwd()
        self.results_dir = os.path.join(self.main_dir, 'Results')
        self.dict_dir = os.path.join(self.main_dir, 'Dictionary')
        self.data_dir = os.path.join(self.main_dir, 'Data')
        self.expr_dir = os.path.join(self.results_dir,self.experiment_name)
        # Check if experiment directory is available, if not make one
        try:
            os.listdir(self.expr_dir)
        except:
            os.mkdir(self.expr_dir)
        # Identify version of the run/experiment
        self.expr_versions_ls = self.get_current_version(self.expr_dir,add_new_version = True)
        
        # Make version directory for results and log
        if self.overwrite_existing and len(self.expr_versions_ls)>1:
            self.expr_versions_ls.pop()
            self.expr_v_dir = os.path.join(self.expr_dir,self.expr_versions_ls[-1])
        else:
            os.mkdir(self.expr_v_dir)
        self._initiate_log()
        print('Experiment directory is created: %s' %self.expr_v_dir)
        if len(self.expr_versions_ls) == 1:
            print('Currently %d version is available.' %len(self.expr_versions_ls) )
        elif len(self.expr_versions_ls) > 1:
            print('Currently %d versions are available.' %len(self.expr_versions_ls) )
        print('Current version: %s' %self.expr_versions_ls[-1] )

    def get_current_version(self, path_dir, file_name = None, add_new_version = False):
        '''
        Returns a list of available versions, last entry would be the current version.
        '''
        list_of_versions = os.listdir(path_dir)
        if file_name and '.' in file_name:
            list_of_versions = [x for x in list_of_versions if re.search(file_name[:file_name.rfind('.')] + '_v\d+.[a-zA-Z0-9]',x, re.IGNORECASE)]
        elif file_name and '.' not in file_name:
            list_of_versions = [x for x in list_of_versions if re.search(file_name[:] + '_v\d+.[a-zA-Z0-9]',x, re.IGNORECASE)]
        if len(list_of_versions) == 0:
            if add_new_version:
                if file_name is not None:
                    try:
                        list_of_versions.append(file_name[:file_name.rfind('.')] + '_v1' + file_name[file_name.rfind('.'):])
                    except:
                        raise Exception("Cannot make new version as no such file is available. Try giving full name with extension.")
                else:
                    list_of_versions.append('v1')
            else:
                raise Exception('No such file or directory.')
        else:
            curr_v = max([int(re.search('(?i)v(\d+)',x, re.IGNORECASE)[1]) for x in list_of_versions])
            if add_new_version:
                curr_v = 'v' + str(curr_v + 1)
                list_of_versions.append(curr_v)
                if file_name is not None:
                    list_of_versions[-1] = self._replace_version(list_of_versions[0],curr_v)


        list_of_versions.sort() 
        return list_of_versions

    def read_data(self,file_name, version = 'latest'):
        # Specify data directory
        file_name = file_name.lower()
        if 'dict' in file_name:
            file_path = self.dict_dir
        else:
            file_path = self.data_dir
        
        data_versions = self.get_current_version(file_path, file_name)
        
        if version == 'latest':
            file_name_with_v = data_versions[-1]
        else:
            if isinstance(version,int):
                version = 'v' + str(version)
            file_name_with_v = self._replace_version(data_versions[0], version.lower())
        
        try:
            data = pd.read_excel(os.path.join(file_path,file_name_with_v))
        except:
            pass
            try:
                data = pd.read_csv(os.path.join(file_path,file_name_with_v))
            except:
                raise Exception('No such file or directory exists. Please make sure the data is either in csv or xlsx format.')
        
        print('Data read successfully, data name: %s, verion: %s.' %(file_name_with_v, version))
        return data
    
    def read_logged_file(self,file_name, version = 'latest', sheet_name = 0):
        # Specify data directory
        file_name = file_name.lower()
        file_path = self.expr_v_dir
        
        data_versions = self.get_current_version(file_path, file_name)
        
        if version == 'latest':
            file_name_with_v = data_versions[-1]
        else:
            if isinstance(version,int):
                version = 'v' + str(version)
            file_name_with_v = self._replace_version(data_versions[0], version.lower())
        
        try:
            data = pd.read_excel(os.path.join(file_path,file_name_with_v), sheet_name  = sheet_name)
        except:
            pass
            try:
                data = pd.read_csv(os.path.join(file_path,file_name_with_v))
            except:
                raise Exception('No such file or directory exists. Please make sure the data is either in csv or xlsx format.')
        return data
    
    def log_file(self, file_name):
        file_ls = self.get_current_version(self.expr_v_dir,file_name, add_new_version= True)
        return os.path.join(self.expr_v_dir,file_ls[-1])

    def _initiate_log(self):
        ############ Print Log
        self._old_stdout = sys.stdout
        # Make log file
        self.log_file_name = open(os.path.join(self.expr_v_dir, self.log_file_name + '.log'),'w')
        sys.stdout = self.log_file_name
    
    def _replace_version(self,file_name_full_with_extension, curr_v):
        pattern = 'v\d+' +'(?!.*v\d+)'
        return re.sub(pattern,curr_v ,file_name_full_with_extension)

    def close_expr(self):
        sys.stdout = self._old_stdout
        self.log_file_name.close()
