import pandas as pd
import dill as pickle
from sklearn import ensemble
from sklearn.model_selection import GridSearchCV


def preprocess_time(dataset):
    dataset['time'] = pd.to_datetime(dataset.fecha + " " + dataset.hora, format="%Y-%m-%d %H:%M:%S.%f")
    dataset['fecha'] = pd.to_datetime(dataset.fecha, format="%Y-%m-%d")
    dataset['hora'] = pd.to_datetime(dataset.hora, format="%H:%M:%S.%f")
    dataset['dow'] = dataset['fecha'].apply(lambda fecha: fecha.weekday())
    dataset = dataset[dataset['dow'] != 6]

    time_start = pd.to_datetime('10:00:00.000000', format="%H:%M:%S.%f")
    time_end = pd.to_datetime('19:59:00.000000', format="%H:%M:%S.%f")
    mask = (time_start <= dataset['hora']) & (dataset['hora'] < time_end)
    dataset = dataset[mask]
    return dataset


def get_count(df, column_name):
    df = df.set_index('time')
    df = df.groupby(by=['id_cuadra', pd.Grouper(freq='15Min')]).count()
    df = df[df['operacion'] != 0]
    df[column_name] = df['operacion']
    df = df.drop(['operacion', 'patente', 'tarjeta', 'direccion', 'dow'], axis=1)
    return df


def get_total_spaces(cant_lugares, id_cuadra):
    return cant_lugares.at[id_cuadra, 'cant_espacios']


def get_places_by_block():
    cant_lugares = pd.read_csv("../data/cant_espacios.csv")
    cant_lugares = cant_lugares[['id_cuadra', 'cant_espacios']]
    cant_lugares = cant_lugares.set_index('id_cuadra')
    return cant_lugares


def get_spaces_time(df, cant_lugares):
    prev_date = "1900-00-00"
    prev_cuadra = 0
    total_spaces = 0
    ret = []
    partial_sum = 0
    available = 0
    for row in df.iterrows():
        # row[0][0] id_cuadra
        # row[0][1] time
        # row[1][0] count_in
        # row[1][1] count_out
        id_cuadra = row[0][0]
        date = row[0][1]
        splitted = str(row[0][1]).split()
        if prev_cuadra != id_cuadra:
            total_spaces = get_total_spaces(cant_lugares, id_cuadra)
            prev_cuadra = id_cuadra
        if prev_date != splitted[0]:
            available = total_spaces
            prev_date = splitted[0]
            partial_sum = available

        partial_sum = partial_sum - row[1][0] + row[1][1]
        ret.append(partial_sum)
    df['available'] = ret
    df['total'] = df.apply(lambda row: get_total_spaces(cant_lugares, row.name[0]), axis=1)


def get_avr(available, total):
    avr = (available / total)
    if avr > 1:
        return 1
    return avr


def preprocess(dataset):
    print("Preprocessing")
    dataset = dataset.sort_values(['fecha', 'hora'])

    dataset = preprocess_time(dataset)
    dataset = dataset[dataset['id_cuadra'] != 50]
    dataset = dataset.drop('hora', axis=1)
    dataset = dataset.drop('fecha', axis=1)
    dataset['time'] = dataset['time'].dt.round('15min')

    dfi = dataset[dataset['operacion'] == 'Entrada']
    dfo = dataset[dataset['operacion'] == 'Salida']
    dfi = get_count(dfi, "count_in")
    dfo = get_count(dfo, "count_out")

    dataset = pd.merge(dfi, dfo, left_index=True, right_index=True, how='left')
    dataset = dataset.fillna(0, axis=1)
    dataset['count_out'] = dataset.count_out.astype(int)
    dataset['count_in'] = dataset.count_in.astype(int)

    get_spaces_time(dataset, get_places_by_block())
    dataset['avr'] = dataset.apply(lambda row: get_avr(row.available, row.total), axis=1)
    dataset = dataset.reset_index()
    dataset = dataset[['id_cuadra', 'time', 'avr']]
    dataset['dow'] = dataset['time'].dt.dayofweek
    dataset['time'] = dataset['time'].apply(lambda time: get_index(str(time).split()[1]))
    return dataset.copy()


def train_model(X_train, y_train):
    print("Training model")
    model = ensemble.GradientBoostingRegressor()
    # parameters = {'n_estimators': [500], 'max_depth': [3,5,7], 'min_samples_split': [2,4,6,8],
    #               'min_samples_leaf': [4], 'max_features': [0.2], 'random_state': [0,1] }
    parameters = {'n_estimators': [500], 'max_depth': [5], 'min_samples_split': [4],
                  'min_samples_leaf': [4], 'max_features': [0.2], 'random_state': [1]}
    grid = GridSearchCV(model, parameters, cv=5, scoring='r2')
    grid.fit(X_train, y_train)
    return grid


def build_and_train():
    dataset = pd.read_csv("../data/BD_parking_with_address.csv")
    dataset = preprocess(dataset)
    labels = dataset['avr']
    dataset = dataset.drop('avr', axis=1)

    # X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.25, random_state=1)

    grid = train_model(dataset, labels)
    return grid


def dump_model():
    model = build_and_train()
    filename = 'model.pkl'
    with open('../models/' + filename, 'wb') as file:
        pickle.dump(model, file)
        print("Model dumped")


# if __name__ == '__main__':
#     dump_model()
