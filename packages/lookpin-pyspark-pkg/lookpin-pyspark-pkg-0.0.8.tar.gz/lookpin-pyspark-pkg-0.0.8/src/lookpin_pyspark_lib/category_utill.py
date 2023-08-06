
def get_category_unique_key(x):
    return x.division1 + '/' + x.division2

def category_dataframe_to_dict(df):
    dict = {}
    collected = df.collect()
    for row in collected:
        dict[row['division1'] + '/' + row['division2']] = row['id']

    print(dict)
    return dict

