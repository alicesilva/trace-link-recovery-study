import pandas as pd
import numpy as np

class ZeroR_Model:
    def __init__(self, oracle):
        self.oracle = oracle
        self.name = None
        self.gen_name = "zero_r"
    
    def set_name(self, name):
        self.name = name
    
    def get_model_gen_name(self):
        return self.gen_name
    
    def recover_links(self):
        major_target_artifact = self._get_major()
        print('major_target_artifact: {}'.format(major_target_artifact))
        
        self._sim_matrix = []
        for idx,row in self.oracle.iterrows():
            #print('idx: {}'.format(idx))
            if idx in major_target_artifact:
                self._sim_matrix.append([1 for i in range(len(self.oracle.columns))])
            else:
                self._sim_matrix.append([0 for j in range(len(self.oracle.columns))])
        
        self._sim_matrix = pd.DataFrame(data=self._sim_matrix, index=self.oracle.index, columns=self.oracle.columns)
        
        #display(self._sim_matrix)
    
    def _get_major(self):
        counts = self.oracle.apply(lambda row : np.sum(row), axis=1)
        df_aux = pd.DataFrame(data=zip(self.oracle.index,counts))
        df_aux.sort_values(by=1, inplace=True, ascending=False)
        max_ = df_aux.iloc[0,1]
        max_counts_df = df_aux[df_aux[1] == max_]
        return list(max_counts_df.iloc[:,0])
        
    def get_sim_matrix(self):
        return self._sim_matrix