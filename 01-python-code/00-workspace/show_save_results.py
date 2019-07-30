def show_save_results(results, filename='final-results.csv'):
    '''
    function to print and export modelling results
    '''
    display(pd.DataFrame.from_dict(results).T)
    print(pd.DataFrame.from_dict(results).T.to_latex())
    pd.DataFrame.from_dict(results).T.to_csv(filename)