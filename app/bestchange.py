import os
import urllib.request as ur
import urllib.parse as up
import zipfile
import csv
import json


class Bestchange:

    """
    Класс для работы с сервисом bestchange.ru
    """

    BCH_URL = 'http://api.bestchange.ru/info.zip'

    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir

        if not os.path.isdir(self.tmp_dir):
            os.mkdir(self.tmp_dir)

        self.update_datafile()

    @staticmethod
    def read_csv(filename):
        """Возвращаем список списков данных из csv файлов"""
        with open(filename, 'rt', encoding='cp1251') as fout:
            iter_list = csv.reader(fout, delimiter=';')
            data = [row for row in iter_list]

        return data

    def update_datafile(self):
        """Скачиваем архив с данными и распаковываем его"""
        path = self.tmp_dir + up.urlparse(self.BCH_URL).path

        # with ur.urlopen(BCH_URL) as best:
        #    header = best.getheader('Last-Modified')
        #    st_obj = time.strptime(header, '%a, %d %b %Y %H:%M:%S GMT')
        #    last_mod_new = time.mktime(st_obj)

        result = ur.urlretrieve(self.BCH_URL, path)
        with zipfile.ZipFile(path, 'r') as arch:
            arch.extractall(path=self.tmp_dir)

        return result

    def get_currencys(self):
        """
        Возвращает словарь - {Id: Название валюты}

        bm_cy.dat – список валют в формате:
        Id валюты; xx; название валюты; xx; xx; xx; xx
        """
        bm_cy = Bestchange.read_csv(self.tmp_dir + '/bm_cy.dat')
        currencys = dict([cur[0:4:2] for cur in bm_cy])

        return currencys

    def get_exchangers(self):
        """
        Возвращает словарь - {Id: Название обменника}

        bm_exch.dat – список обменников в формате:
        Id обменника; название обменника; xx; xx; xx
        """
        bm_exch = Bestchange.read_csv(self.tmp_dir + '/bm_exch.dat')
        exchangers = dict([exch[0:2] for exch in bm_exch])

        return exchangers

    def get_rates(self):
        """
        Возвращаем список списков курса обмена с подставленными в него названиями валют и обменников

        bm_rates.dat – список курсов обмена в формате:
        ID отдаваемой валюты; ID получаемой валюты; ID обменника; курс обмена (отдать); курс обмена (получить);
            резерв получаемой валюты; отзывы; xx
        """
        currencys = self.get_currencys()
        exchangers = self.get_exchangers()

        bm_rates = Bestchange.read_csv(self.tmp_dir + '/bm_rates.dat')
        excharge_rates = list()
        for rate in bm_rates:
            give = currencys[rate[0]]
            get = currencys[rate[1]]
            exchanger = exchangers[rate[2]]
            # Валюта отдаем, валюта получаем, название обменника, сколько отдаем, сколько получаем, резерв,
            #    отзывы плохие.хорошие
            excharge_rates.append([give, get, exchanger, rate[3], rate[4], rate[5], rate[6].replace('.', '/')])

        return excharge_rates


if __name__ == '__main__':
    bestchange = Bestchange('tmp')
    rates = bestchange.get_rates()
    print(json.dumps(rates[0:11], ensure_ascii=False))
