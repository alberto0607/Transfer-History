import os
from dotenv import load_dotenv
from beem import Hive
from beem.account import Account
from beem.amount import Amount
from datetime import datetime, timedelta
from tabulate import tabulate
import matplotlib.pyplot as plt

load_dotenv('.env')

# Carga las variables de entorno desde el archivo .env
hived_nodes = os.getenv("HIVED_NODES").split(',')

# Inicializa la conexión a la blockchain de Hive
hive = Hive(node=hived_nodes)

# Obtener los días trancurridos a partir de una fecha


def days_elapsed():
    start_date_str = os.getenv("START_DATE")
    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        current_date = datetime.now().date()
        elapsed = (current_date - start_date).days
        return elapsed
    else:
        return None


def read_usernames(filename):
    # Lee los nombres de usuario desde un archivo de texto
    with open(filename, 'r') as file:
        usernames = [line.strip() for line in file.readlines()]
    return usernames

# Obtiene el historial de transferencias para cada usuario


def get_transfer_data(users, stop_days):
    transfer_data = {}
    for username in users:
        account = Account(username, blockchain_instance=hive)
        transfers = account.history_reverse(
            stop=stop_days, only_ops=['transfer'])
        hive_sent = 0
        hive_received = 0
        hbd_sent = 0
        hbd_received = 0
        for transfer in transfers:
            amount = Amount(transfer['amount'])
            # Verifica si la transferencia es en HIVE o HBD y suma los montos correspondientes
            if amount.symbol == 'HIVE':
                if transfer['from'] == username:
                    hive_sent += amount.amount
                elif transfer['to'] == username:
                    hive_received += amount.amount
            elif amount.symbol == 'HBD':
                if transfer['from'] == username:
                    hbd_sent += amount.amount
                elif transfer['to'] == username:
                    hbd_received += amount.amount
        # Redondea los montos a 3 decimales
        hive_sent = round(hive_sent, 3)
        hive_received = round(hive_received, 3)
        hbd_sent = round(hbd_sent, 3)
        hbd_received = round(hbd_received, 3)
        # Almacena los datos de transferencia en un diccionario para cada usuario
        transfer_data[username] = {
            'HIVE Sent': hive_sent,
            'HIVE Received': hive_received,
            'HBD Sent': hbd_sent,
            'HBD Received': hbd_received
        }

    # Ordena los datos de transferencia por el monto recibido en HBD en orden descendente
    transfer_data = {k: v for k, v in sorted(
        transfer_data.items(), key=lambda item: item[1]['HBD Received'], reverse=True)}

    return transfer_data

# Obtiene el historial de transferencias mensual


def get_transfer_data_by_month(users, stop_days):
    data_by_month = {}

    for username in users:
        account = Account(username, blockchain_instance=hive)

        transfers = account.history_reverse(
            stop=stop_days, only_ops=['transfer'])
        for transfer in transfers:
            timestamp = datetime.fromisoformat(transfer['timestamp'])
            year_month = timestamp.strftime("%Y-%m")
            amount = Amount(transfer['amount'])
            if year_month not in data_by_month:
                # Inicializa los valores de transferencia para cada mes
                data_by_month[year_month] = {
                    'HIVE Sent': 0,
                    'HIVE Received': 0,
                    'HBD Sent': 0,
                    'HBD Received': 0
                }
            # Actualiza los montos de transferencia para cada mes
            if amount.symbol == 'HIVE':
                if transfer['from'] == username:
                    data_by_month[year_month]['HIVE Sent'] += amount.amount
                elif transfer['to'] == username:
                    data_by_month[year_month]['HIVE Received'] += amount.amount
            elif amount.symbol == 'HBD':
                if transfer['from'] == username:
                    data_by_month[year_month]['HBD Sent'] += amount.amount
                elif transfer['to'] == username:
                    data_by_month[year_month]['HBD Received'] += amount.amount

    for year_month, values in data_by_month.items():
        # Redondea los montos a 3 decimales
        values['HIVE Sent'] = round(values['HIVE Sent'], 3)
        values['HIVE Received'] = round(values['HIVE Received'], 3)
        values['HBD Sent'] = round(values['HBD Sent'], 3)
        values['HBD Received'] = round(values['HBD Received'], 3)

    # Ordena los datos por fecha ascendente
    data_by_month = dict(sorted(data_by_month.items(),
                                key=lambda x: x[0], reverse=False))

    return data_by_month

# Crea una tabla de usuarios con los datos de transferencia


def create_table_users(data, headers):
    table_data = [[username, data[username]['HIVE Sent'], data[username]['HIVE Received'],
                   data[username]['HBD Sent'], data[username]['HBD Received']] for username in data.keys()]
    # Calcula los totales de los montos de transferencia
    totals = ['Total', sum(data[username]['HIVE Sent'] for username in data.keys()), sum(data[username]['HIVE Received'] for username in data.keys(
    )), sum(data[username]['HBD Sent'] for username in data.keys()), sum(data[username]['HBD Received'] for username in data.keys())]
    table_data.append(totals)
    # Genera la tabla en formato Markdown
    return tabulate(table_data, headers, tablefmt='pipe')

# Guarda la tabla en un archivo


def save_table(table, filename):
    with open(filename, 'w') as file:
        file.write(table)

 # Crea una tabla mensual con los datos de transferencia


def create_table_month(data, headers):
    table_data = [[month] + [data[month][key]
                             for key in headers[1:]] for month in data.keys()]
    # Calcula los totales de los montos de transferencia por mes
    totals = ['Total'] + [sum(data[month][key]
                              for month in data.keys()) for key in headers[1:]]
    table_data.append(totals)
    # Genera la tabla en formato Markdown
    return tabulate(table_data, headers, tablefmt='pipe')

# Guardar la tabla mensual en un archivo


def save_table_month(table, filename):

    with open(filename, 'w') as file:
        file.write(table)

# Generar gráfica de barras horrizontales de las transferencias de usuarios


def graph_users_hbd_received(data):
    usernames = list(data.keys())
    hbd_received = [data[user]['HBD Received'] for user in usernames]

    plt.figure(figsize=(12, 8))
    plt.barh(range(len(usernames)), hbd_received, align='center')
    plt.yticks(range(len(usernames)), usernames)
    plt.title('HBD Received by User')
    plt.xlabel('Amount')
    plt.ylabel('Users')
    plt.savefig('graph_users_hbd_received.png')

# Generar gráfica de barras verticales de las transferencias mensuales


def graph_month(data):
    months = list(data.keys())
    hive_sent = [data[month]['HIVE Sent'] for month in months]
    hive_received = [data[month]['HIVE Received'] for month in months]
    hbd_sent = [data[month]['HBD Sent'] for month in months]
    hbd_received = [data[month]['HBD Received'] for month in months]

    plt.figure(figsize=(12, 6))
    plt.bar(months, hive_sent, label='HIVE Sent')
    plt.bar(months, hive_received, label='HIVE Received')
    plt.bar(months, hbd_sent, label='HBD Sent')
    plt.bar(months, hbd_received, label='HBD Received')
    plt.title('Transaction Amounts by Month')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.legend()
    plt.savefig('graph_month.png')


def main():

    day = days_elapsed()

    users_filename = 'users.txt'
    usernames = read_usernames(users_filename)
    stop_days = datetime.utcnow() - timedelta(days=day)

    # Obtener los datos de transferencia para los usuarios y los guarda en un diccionario
    transfer_data = get_transfer_data(usernames, stop_days)
    print(transfer_data)

    print('##############################')

    # Obtener los datos de transferencia agrupados por mes y guarda en un diccionario
    data_month = get_transfer_data_by_month(usernames, stop_days)
    print(data_month)

    headers = ['Username', 'HIVE Sent',
               'HIVE Received', 'HBD Sent', 'HBD Received']
    # Crear la tabla de usuarios, la gráfica y muestra los resultados
    table_users = create_table_users(transfer_data, headers)
    graph_users_hbd_received(transfer_data)
    print(table_users)
    # Guardar la tabla de usuarios en un archivo
    save_table(table_users, 'table_users.txt')

    headers_month = ['Month', 'HIVE Sent',
                     'HIVE Received', 'HBD Sent', 'HBD Received']
    # Crear la tabla mensual, la gráfica y muestra los resultados
    table_month = create_table_month(data_month, headers_month)
    graph_month(data_month)
    print(table_month)

    # Guardar la tabla mensual en un archivo
    save_table_month(table_month, 'table_month.txt')


if __name__ == '__main__':
    main()
