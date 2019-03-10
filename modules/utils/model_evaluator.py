import pandas as pd
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.metrics import precision_recall_fscore_support
import pprint
import pickle
import math

class ModelEvaluator:
    def __init__(self, oracle, model):
        self.model = model
        self.oracle = oracle
                
        self.evaluator_dump_path = None
        
        self.eval_df = pd.DataFrame(columns=['precision','recall','fscore','support'])
        self.mean_precision = -1
        self.mean_recall = -1
        self.mean_fscore = -1
        
        self.set_evaluator_dump_path()
    
        
    def __fillUp_traceLinksDf(self, top_n, sim_threshold):
        trace_links_df = pd.DataFrame(index = self.model.get_sim_matrix().index,
                                      columns = self.model.get_sim_matrix().columns,
                                      data = self.model.get_sim_matrix().values)
        
        for col in trace_links_df.columns:
            nlargest_df = trace_links_df.nlargest(n = top_n, columns=col, keep='first')    
            trace_links_df[col] = [1 if x in nlargest_df[col].tolist() and x >= sim_threshold[1] else 0 for x in trace_links_df[col]]

        return trace_links_df
    
    def evaluate_model(self, verbose=False, file=None, top_value=None, sim_threshold=None, ref_name=""):
        print("\n {} Evaluation - {}".format(self.model.get_name(), ref_name))
        
        recovered_links = self.__fillUp_traceLinksDf(top_n=top_value, sim_threshold=sim_threshold)
        
        y_true = csr_matrix(self.oracle.values, dtype='int8')
        y_pred = csr_matrix(recovered_links.values, dtype='int8')
        
        p, r, f, sp = precision_recall_fscore_support(y_true, y_pred)

        i = 0
        for idx, row in self.oracle.iteritems():
            self.eval_df.at[idx, 'precision'] = p[i]
            self.eval_df.at[idx, 'recall'] = r[i]
            self.eval_df.at[idx, 'fscore'] = f[i]
            self.eval_df.at[idx, 'support'] = sp[i]
            i += 1
        
        self.mean_precision = self.eval_df.precision.mean()
        self.mean_recall = self.eval_df.recall.mean()
        self.mean_fscore = self.eval_df.fscore.mean()
        
        if verbose:
            self.print_report(file)
        
        return (ref_name, round(self.mean_precision,2), round(self.mean_recall,2), round(self.mean_fscore,2))
            
       
    def print_report(self, file=None):
        dic = self.model.model_setup()
        dic['Measures'] = {}
        dic['Measures']['Mean Precision of {}'.format(self.model.get_name())] = self.get_mean_precision()
        dic['Measures']['Mean Recall of {}'.format(self.model.get_name())] = self.get_mean_recall()
        dic['Measures']['Mean FScore of {}'.format(self.model.get_name())] = self.get_mean_fscore()
        
        if file is None:    
            pprint.pprint(dic)
        else:
            file.write(pprint.pformat(dic))
        
    def plot_precision_vs_recall(self):
        plt.figure(figsize=(6,6))
        plt.plot(self.eval_df.recall, self.eval_df.precision, 'ro', label='Precision vs Recall')

        plt.ylabel('Precision')
        plt.xlabel('Recall')

        plt.axis([0, 1.1, 0, 1.1])
        plt.title("Precision vs Recall Plot - " + self.model.get_name())
        plt.show()
    
    def save_log(self):
        print("\nSaving model log...")
        with open('../logs/' + str(datetime.datetime.now()) + '.txt', 'a') as f:
            evaluator.evaluate_model(verbose=True, file=f)
        print("Model log saved with success!")
            
    def get_mean_precision(self):
        return self.mean_precision
    
    def get_mean_recall(self):
        return self.mean_recall
    
    def get_mean_fscore(self):
        return self.mean_fscore

    def get_model(self):
        return self.model
    
    def get_evaluator_dump_path(self):
        return self.evaluator_dump_path
    
    def dump_evaluator(self):
        pickle.dump(self, open(self.get_evaluator_dump_path(), 'wb'))
        
    def dump_model(self):
        pickle.dump(self.get_model(), open(self.get_model().get_model_dump_path(), 'wb'))
        
    def set_evaluator_dump_path(self):
        self.evaluator_dump_path = 'dumps/{}/evaluator/eval_{}.p'.format(self.get_model().get_model_gen_name(), self.get_model().get_name())