def count_total_questions(dataArray, datasetDict):
    '''
    function to count total questions across fora
    '''
    # initiate counter for total number
    s = 0
    
    # print number per fora
    for i in dataArray:
        s = s + datasetDict[i].count()
        print(f'{i}: {datasetDict[i].count()}')
    
    # print total number
    print(f'\nTotal: {s}')