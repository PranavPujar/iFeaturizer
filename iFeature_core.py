import numpy as np
import pandas as pd
import os
from sys import platform
from functools import reduce

#add support for Linux and OS X  

class iFeature_set:
    def __init__(self, in_path, in_file, in_fasta_col_name, iFeature_dir):

        #Directory to store initial and postprocessed output TSV files
        self.tsv_dir = os.path.dirname(in_path)
        self.postprocessed_dir = "{}/postprocessed".format(os.path.dirname(in_path))
        try:
            os.mkdir(self.postprocessed_dir)
        except FileExistsError:
            pass

        #Paths of intermediate files
        self.protein_path = "{}/protein.txt".format(os.path.dirname(in_path))
        self.bat_path = "{}/run.bat".format(os.path.dirname(in_path))

        #Iterable containing all FASTA sequences to extract features from 
        self.fasta = in_file[in_fasta_col_name]
                
        #Directory containing iFeature.py and helper modules
        self.iFeature_dir = iFeature_dir
        
        #21 feature descriptor types 
        self.feature_descriptors = ['AAC', 'APAAC', 'CKSAAGP', 'CKSAAP', 'CTDC']#, 'CTDD', \
                                    # 'CTDT', 'CTriad', 'DDE', 'DPC', 'GAAC', 'GDPC', 'Geary', \
                                    # 'GTPC', 'KSCTriad', 'Moran', 'NMBroto', 'PAAC', 'QSOrder', \
                                    # 'SOCNumber', 'TPC']


    def generate_intermediate_files(self):
        
        #Generate protein.txt
        with open(self.protein_path, 'w+') as protein:
            for i in range(len(self.fasta)):
                protein.write('>Cas_sequence_{}\n{}\n'.format(i, self.fasta[i]))
        
        #Generate run.bat
        with open(self.bat_path, 'w+') as bat_file:

            #cd to iFeature dir to run subsequent commands
            bat_file.write('cd {}\n'.format(self.iFeature_dir))
            
            #iterating through each feature - 21 iterations in total, to write 21 commands into .bat
            for f_type in self.feature_descriptors:
                bat_file.write('python iFeature.py --file {0} --type {1} --out {2}/{1}.tsv\n'.format(self.protein_path, f_type, self.postprocessed_dir))

        
    def extract(self):
        os.system(self.bat_path)
    

    def postprocess_and_merge(self, destination_dir, df_merged_name="df_merged", out_type="tsv"):
        df_list = list()

        #Some data postprocessing to allow for correct merging and fit input requirements for ML models 
        for f_type in self.feature_descriptors:
            #reading
            df = pd.read_csv('{}/{}.tsv'.format(self.postprocessed_dir, f_type), sep = '\t')
            df = pd.concat([df[:1], df]) #duplicate 0th row
            df.iloc[0] = f_type
            
            df.reset_index(inplace=True)
            df.drop('index', axis=1, inplace=True)
            df['#'][0] = np.NaN
            
            df.to_csv('{}/{}.tsv'.format(self.postprocessed_dir, f_type), sep='\t')
            df_list.append(df)

            #Merging the 21 pd.DataFrame objects
            data_merged = reduce(lambda left, right: pd.merge(left , right, on = ["#"]), df_list)

            #Output to TSV/CSV in the pre-defined directory
            if out_type == "csv":
                data_merged.to_csv('{}/{}.{}'.format(destination_dir, df_merged_name, out_type))
            else:
                data_merged.to_csv('{}/{}.{}'.format(destination_dir, df_merged_name, out_type), sep='\t')

            os.chdir(destination_dir)

            #Vary commands as per native OS
            native_os = platform.system()
            # if native_os == 'Windows':
            os.system('tar -a -c -f {0}.zip {0}.{1}'.format(df_merged_name, out_type)) #Make Mac-compatible as well
            os.system('rm {}.{}'.format(df_merged_name, out_type))