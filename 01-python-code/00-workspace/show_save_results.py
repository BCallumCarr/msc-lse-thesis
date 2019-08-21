def show_save_results(results, filename='final-results.csv'):
    '''
    function to print and export modelling results
    '''
    # display nice pd dataframe in notebook
    display(pd.DataFrame.from_dict(results).T)

    # output latex to copy into article
    print(pd.DataFrame.from_dict(results).T.to_latex())

    # export to csv
    pd.DataFrame.from_dict(results).T.to_csv(filename)