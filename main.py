from datetime import datetime

records = [
    {
        "source": "48-996355555",
        "destination": "48-666666666",
        "end": 1564610974,
        "start": 1564610674,
    },
    {
        "source": "41-885633788",
        "destination": "41-886383097",
        "end": 1564506121,
        "start": 1564504821,
    },
    {
        "source": "48-996383697",
        "destination": "41-886383097",
        "end": 1564630198,
        "start": 1564629838,
    },
    {
        "source": "48-999999999",
        "destination": "41-885633788",
        "end": 1564697158,
        "start": 1564696258,
    },
    {
        "source": "41-833333333",
        "destination": "41-885633788",
        "end": 1564707276,
        "start": 1564704317,
    },
    {
        "source": "41-886383097",
        "destination": "48-996384099",
        "end": 1564505621,
        "start": 1564504821,
    },
    {
        "source": "48-999999999",
        "destination": "48-996383697",
        "end": 1564505721,
        "start": 1564504821,
    },
    {
        "source": "41-885633788",
        "destination": "48-996384099",
        "end": 1564505721,
        "start": 1564504821,
    },
    {
        "source": "48-996355555",
        "destination": "48-996383697",
        "end": 1564505821,
        "start": 1564504821,
    },
    {
        "source": "48-999999999",
        "destination": "41-886383097",
        "end": 1564610750,
        "start": 1564610150,
    },
    {
        "source": "48-996383697",
        "destination": "41-885633788",
        "end": 1564505021,
        "start": 1564504821,
    },
    {
        "source": "48-996383697",
        "destination": "41-885633788",
        "end": 1564627800,
        "start": 1564626000,
    },
]


def accounting_customers(records):
    """
    Função que contabiliza quantos clientes existem no registro e retorna
    um array com esses clientes
    :param records:
    :return customers:
    """
    customers = []

    # Loop que coloca os nomes dentro do array e verifica se o nome ja existe
    for record in records:
        if record['source'] not in customers:
            customers.append(record['source'])

    return customers


def value_by_phone_number(customers):
    """
    Função que constrói o array que receberá o valor total que será
    cobrado a cada cliente
    :param customers:
    :return total_values:
    """
    total_values = []

    # Loop que modificará o array total_values
    for number in customers:
        total_values.append({'source': number, 'total': 0})

    return total_values


def prepares_return(data_filter, total_values):
    """
    Funcção que prepara o array final com os valores totais por cliente
    :param data_filter:
    :param total_values:
    :return total_values:
    """
    for number in total_values:
        for record in data_filter:
            if number['source'] == record['source']:
                number['total'] += record['valor']

        # Arredondando os valores
        number['total'] = round(number['total'], 2)

    return total_values


def check_shift(start_time, end_time, final_minute, starting_minute, record):
    """
    Função que verifica o turno da chamada e calcula o valor da ligação
    :param start_time:
    :param end_time:
    :param final_minute:
    :param starting_minute:
    :return value:
    """

    nem_start_time = start_time + (starting_minute / 60)
    nem_end_time = end_time + (final_minute / 60)

    call_time = (record['end'] - record['start']) // 60

    if 6 < nem_start_time < 22:
        if 6 < nem_end_time < 22:
            # Portanto a ligação foi completada no periodo diurno
            value = 0.36 + call_time * 0.09
        else:
            # Portanto a ligação iniciou no periodo diurno e terminou
            # no periodo noturno
            hour_max = 22
            value = 0.36 + ((hour_max - nem_start_time) * 60) * 0.09
            value = value + 0.36
    else:
        if not 6 < nem_end_time < 22:
            # Portanto a ligação foi completada no periodo noturno
            value = 0.36
        else:
            # Portanto a ligação iniciou no periodo noturno e terminou
            # no periodo diurno
            hour_min = 6
            value = 0.36 + ((nem_end_time - hour_min) * 60) * 0.09
            value = value + 0.36

    return value


def classify_by_phone_number(records):
    # Primeiro criei o array dados_filtrados
    data_filter = []

    # criei uma variavel que recebe a lista com clientes
    customers = accounting_customers(records)

    # criei uma variavel que recebe uma lista com vários dicionarios
    # contendo as chaves 'source' e 'total'
    total_values = value_by_phone_number(customers)

    for record in records:
        # Peguei a hora inicial, hora final, minuto inicial,
        # e minuto final de cada ligação
        start_time = datetime.fromtimestamp(record['start']).hour
        end_time = datetime.fromtimestamp(record['end']).hour
        final_minute = datetime.fromtimestamp(record['end']).minute
        start_minute = datetime.fromtimestamp(record['start']).minute

        # Variavel que recebe o valor da ligação
        value = check_shift(start_time, end_time, final_minute, start_minute, record)

        # Depois coloquei na lista os dados filtrados com o cliente e o valor
        data = {'source': record['source'], 'valor': value}
        data_filter.append(data)

    # colocar o valor no total em total_values
    total_values = prepares_return(data_filter, total_values)

    # Ordenando valores
    valores_ordenados = sorted(total_values,
                               key=(lambda k: k['total']),
                               reverse=True)

    return valores_ordenados

