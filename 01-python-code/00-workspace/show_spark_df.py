def show_spark_df(df, n=5):
    '''
    function to better print spark df entries
    '''
    display(pd.DataFrame(df.head(n), columns=df.columns))