import pandas as pd

def covert_nan(x):
    
    if pd.isna(x):
        return ""
    else:
        return str(x)
    
def Combine_Col(dataset, col_1, col_2):
    
    df_col_1_2 = pd.DataFrame(dataset[col_1]+ '. ' + dataset[col_2].map(covert_nan),columns=[col_1+'_'+col_2])
    new_dataset = pd.concat([df_col_1_2,dataset],axis=1)
    
    return new_dataset