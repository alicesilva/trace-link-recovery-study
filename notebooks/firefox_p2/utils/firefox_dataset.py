import pandas as pd

def read_trace_df():
    oracle_df = pd.read_csv('../../data/mozilla_firefox_v2/firefoxDataset/oracle/output/trace_matrix_final_emp_study.csv')
    oracle_df.set_index('tc_name', inplace=True, drop=True)
    print('Oracle.shape: {}'.format(oracle_df.shape))
    return oracle_df
    
def read_testcases_df():
    testcases_df = pd.read_csv('../../data/mozilla_firefox_v2/firefoxDataset/docs_english/TC/testcases_final.csv')
    print('TestCases.shape: {}'.format(testcases_df.shape))
    return testcases_df

def read_bugreports_df():
    bugreports_df = pd.read_csv('../../data/mozilla_firefox_v2/firefoxDataset/docs_english/BR/selected_bugreports_final.csv')
    print('BugReports.shape: {}'.format(bugreports_df.shape))
    return bugreports_df