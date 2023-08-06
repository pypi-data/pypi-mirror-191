import numpy as np

def read_encoded_csv(csv_path):

    print('[LOG] Reading file: ' + csv_path)
    data_file = open(csv_path, "r")
    features = data_file.readline().split(',')
    features = [f.replace('\n', '').strip() for f in features]
    print(f'[LOG] Number of features in "{csv_path}" :', len(features))
    data = []
    for row in data_file:
        row = row.replace('\n', '').split(',')
        float_row = []
        for x in row:
            float_row.append(float(x))
        data.append(float_row)
    return np.array(features), np.array(data)