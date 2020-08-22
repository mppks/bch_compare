import os
import urllib.request as ur
import urllib.parse as up
import zipfile
import time
import csv
import json
from flask import Flask, render_template

TEMP_DIR = 'tmp'
BCH_URL = 'http://api.bestchange.ru/info.zip'
SLEEP_TIME = 10

def read_csv(filename):
    """Возвращаем список списков данных из csv файлов"""
    with open(filename, 'rt') as fout:
        iter_list = csv.reader(fout, delimiter=';')
        data = [row for row in iter_list]

    return data


def get_dch_datafile():
    """Скачиваем архив с данными и распаковываем его"""
    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    path = TEMP_DIR + up.urlparse(BCH_URL).path

    # with ur.urlopen(BCH_URL) as best:
    #    header = best.getheader('Last-Modified')
    #    st_obj = time.strptime(header, '%a, %d %b %Y %H:%M:%S GMT')
    #    last_mod_new = time.mktime(st_obj)

    result = ur.urlretrieve(BCH_URL, path)
    with zipfile.ZipFile(path, 'r') as arch:
        arch.extractall(path=TEMP_DIR)

    return result


def prep_bch_exch_data():
    """
    Возвращаем список списков курса обмена с подставленными в него названиями валют и обменников

    bm_cy.dat – список валют в формате:
    ID валюты; xx; название валюты; xx; xx; xx; xx

    bm_exch.dat – список обменников в формате:
    ID обменника; название обменника; xx; xx; xx

    bm_rates.dat – список курсов обмена в формате:
    ID отдаваемой валюты; ID получаемой валюты; ID обменника; курс обмена (отдать); курс обмена (получить);
        резерв получаемой валюты; отзывы; xx
    """
    # ID:Название валюты
    currencys = read_csv(TEMP_DIR + '/bm_cy.dat')
    currencys_dict = dict([cur[0:4:2] for cur in currencys])
    #print(currencys_dict)

    # ID:Название обменника
    exchangers = read_csv(TEMP_DIR + '/bm_exch.dat')
    exchangers_dict = dict([exch[0:2] for exch in exchangers])
    #print(exchangers_dict)

    rates = read_csv(TEMP_DIR + '/bm_rates.dat')
    res_rates = list()
    for rate in rates:
        give = currencys_dict[rate[0]]
        get = currencys_dict[rate[1]]
        exchanger = exchangers_dict[rate[2]]
        # Валюта отдаем, валюта получаем, название обменника, сколько отдаем, сколько получаем, резерв,
        #    отзывы плохие.хорошие
        res_rates.append([give, get, exchanger, rate[3], rate[4], rate[5], rate[6]])

    return res_rates


if __name__ == '__main__':
    get_dch_datafile()
    bch_data = prep_bch_exch_data()

    #for row in bch_data:
    #    print(row)

    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('index.html')

    app.run(port=9999, debug=True)

    '''
    quit = True
    print('Try Ctrl+C to exit')
    while quit:
        try:
            print(getBestchange())
            print('Sleep')
            time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            print('finishing...')
            quit = False
    '''