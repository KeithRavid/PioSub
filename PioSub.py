import os

current_directory = os.getcwd()
print("Current Working Directory:", current_directory)


import pandas as pd
data = open('All.txt')
data = data.read().splitlines()
data = pd.DataFrame(data, columns=['Raw'])

data['Card1_Value'] = data['Raw'].str.slice(0,1)
data['Card1_Suit'] = data['Raw'].str.slice(1,2)
data['Card2_Value'] = data['Raw'].str.slice(2,3)
data['Card2_Suit'] = data['Raw'].str.slice(3,4)
data['Card3_Value'] = data['Raw'].str.slice(4,5)
data['Card3_Suit'] = data['Raw'].str.slice(5,6)

numeric = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
data = data.replace(numeric)
data = data.apply(pd.to_numeric, errors='ignore')

def categorize(row):
    #Categorize suits
    if row['Card1_Suit'] == row['Card2_Suit'] == row['Card3_Suit']:
        row['suits'] = 'monotone'
    elif (row['Card1_Suit'] == row['Card2_Suit'] and row['Card1_Suit'] != row['Card3_Suit']) or (row['Card1_Suit'] == row['Card3_Suit'] and row['Card1_Suit'] != row['Card2_Suit']) or (row['Card2_Suit'] == row['Card3_Suit'] and row['Card2_Suit'] != row['Card1_Suit']):
            row['suits'] = 'two tone'
    else:
       row['suits'] = 'rainbow'
    
    #Categorize connected
    c = [row['Card1_Value'], row['Card2_Value'], row['Card3_Value']]
    c.sort(reverse=True)
    gap = ((c[0] - c[1]) + (c[1] - c[2])) - 2
    if gap <=2:
        row['connected'] = True
    elif sum(1 for value in c if value == 14) == 1 and all((num <= 5) or (num == 14) for num in c): 
        row['connected'] = True
    else:
        row['connected'] = False
    return row
data = data.apply(categorize, axis=1)

import re
def generate(userin, high_card):
    subset1 = data
    if 'connected' in userin:
        subset1 = data[data['connected'] == True]
    elif 'nsp' in userin:
        subset1 = data[data['connected'] == False]
    
    if 'monotone' in userin:
        subset = subset1[subset1['suits'] == 'monotone']
    elif 'two tone' in userin:
        subset = subset1[subset1['suits'] == 'two tone']
    elif 'rainbow' in userin:
        subset = subset1[subset1['suits'] == 'rainbow']
    else:
        subset = subset1
        
    if high_card != 'N/A':
        subset = subset[subset['Card1_Value'] == int(high_card)]
    
    num = re.search(r'\b\d+\b', userin)
    num = int(num.group())
    subset = subset.sample(n=num)
    
    output = subset['Raw']
    
    return output


high = input('Enter x high board, A = 14, K = 13, Q = 12, J = 11, or N/A: ')
user = input('Please input a number (optional) and any of the following keywords: connected, nsp, monotone, two tone, rainbow: ')

output = generate(user, high)
output.to_csv('output.txt', header=False, index=False)