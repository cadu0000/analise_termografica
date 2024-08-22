import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

DATA_DIR = ''
data_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.xlsx')]

def categorize_temperature(temp):
    if temp >= 45:
        return 3  
    elif temp >= 25:
        return 2 
    elif temp >= 15:
        return 1 
    else:
        return 0  

def read_process_excel(file_path):
    xls = pd.ExcelFile(file_path)
    dfs = []
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        df['posicao'] = df['posicao'].apply(lambda x: eval(x.replace('(', '').replace(')', '')) if isinstance(x, str) else x)
        df['categoria'] = df['temperatura'].apply(categorize_temperature)
        df[['posicao_x', 'posicao_y']] = df['posicao'].apply(pd.Series)
        
        label_encoder = LabelEncoder()
        df['classificacao_encoded'] = label_encoder.fit_transform(df['classificacao'])
        
        dfs.append(df)
    
    return dfs

for file in data_files:
    file_path = os.path.join(DATA_DIR, file)
    dfs = read_process_excel(file_path)
    
    for df in dfs:
        X = df[['temperatura', 'posicao_x', 'posicao_y']]
        y = df['classificacao_encoded']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        print("\nRelatório de Classificação:")
        print(classification_report(y_test, y_pred))
