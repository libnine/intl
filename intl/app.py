import re, os, urllib, time, dateutil.parser as dparser
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime
from fire import *


script_dir = os.path.dirname(__file__)
debug_log = os.path.join(script_dir, 'debug.log')

fire = Fire()

pool = ThreadPool(4)


def millionize(num, m=1000000, b=1000000000):
    if num >= 1000000000:
        num = float(float(num) / b)
        return '{}b'.format(round(num, 2))
    else:        
        num = float(float(num) / m)
        return '{}m'.format(round(num, 2))


class Foreign:
    def __init__(self):
        self.final_f = []
        self.final_d = []
        self.kv_d = {}
        self.kv_f = {}
        self.init_urls = fire.urls_stripped()


    def scrape(self, s):
        try:
            symbol = s.split('/')[-1]
            url = s

            if url == "":
                return

            # regex parsing
            html = urllib.urlopen(url)
            html = html.read()

            # fundamentals
            currency = re.compile('<span class="cr_sym">(.+?)</span>')
            currency = re.findall(currency, html)

            country = re.compile('<span class="exchangeName">(.+?)</span>')
            country = re.findall(country, html)

            try:
                country, exchange = country[0].split(':')
                country = country.replace('(', '')
                exchange = exchange.replace(')', '')
                self.kv_f['country'] = country.strip()
                self.kv_f['exchange'] = exchange.strip()
            except:
                self.kv_f['country'] = "n/a"
                self.kv_f['exchange'] = "n/a"

            price = re.compile('<span id="quote_val">(.+?)</span>')
            price = re.findall(price, html)

            change = re.compile('<span class="cr_num diff_price" id="quote_change">(.+?)</span>')
            change = re.findall(change, html)

            day_range = re.compile('<span class="data_lbl">1 Day Range</span> <span class="data_data">(.+?)</span>')
            day_range = re.findall(day_range, html)

            try:
                hi, lo = [x.strip() for x in day_range[0].split('-')]
            except:
                hi, lo = "n/a", "n/a"
            
            er = re.compile('<span class="metaInfo" id="rr_module_quarterly_meta">(.+?)</span>')
            er = re.findall(er, html)

            try:
                er = re.search(r'\d{2}\/\d{2}\/\d{4}', er[0])
                er = datetime.strptime(er.group(), '%m/%d/%Y').strftime('%m/%d/%Y')
                self.kv_f['er'] = er
            except Exception as e:
                self.kv_f['er'] = "n/a"

            pct_change = re.compile('<span class="cr_num diff_percent" id="quote_changePer">(.+?)</span>')
            pct_change = re.findall(pct_change, html)

            volume = re.compile('<span id="quote_volume" class="data_data">(.+?)</span>')
            volume = re.findall(volume, html)

            try:
                v = float(volume[0].replace(',', ''))
                volume = millionize(int(v))
            except:
                volume = "n/a"

            avg_volume = re.compile('<span class="data_data">(.+?)</span>')
            avg_volume = re.findall(avg_volume, html)

            try:
                av = int(avg_volume[0].replace(',', ''))
                avg_volume = millionize(int(av))
            except:
                avg_volume = "n/a"

            pe = re.compile('<span class="data_data"> (.+?) <small class="data_meta">')
            pe = re.findall(pe, html)

            div_yield = re.compile('<h5 class="data_lbl">Yield</h5> <span class="data_data">(.+?) <small class="data_meta">')
            div_yield = re.findall(div_yield, html)

            try:
                self.kv_f['yield'] = div_yield[0]
            except:
                self.kv_f['yield'] = "n/a"

            try:
                volume_pct = (float(v) / av) * 100
                volume_pct = str(round(volume_pct, 2)) + "%"
            except Exception as e:
                volume_pct = "n/a"

            # create dictionary
            self.kv_f['symbol'] = symbol
            self.kv_d['symbol'] = symbol
            self.kv_f['currency'] = currency[0]
            self.kv_d['price'] = price[0]
            self.kv_d['change'] = change[0]
            self.kv_d['pct_change'] = pct_change[0]
            self.kv_d['low'] = float(lo)
            self.kv_d['high'] = float(hi)
            self.kv_d['volume'] = volume
            self.kv_d['avg_volume'] = avg_volume
            self.kv_d['volume_pct_avg'] = volume_pct
            self.kv_f['pe ratio'] = round(float(pe[0]), 2) if not pe == "" else "n/a"

            self.final_d.append(self.kv_d.copy())
            self.final_f.append(self.kv_f.copy())
        
        except Exception as e:
            print e

        

    def scrape_multi(self, *s):
        if type(s) == tuple:
            s = list(*s)

        if len(s) <= 1:
            self.scrape(s[0])
        else:
            p = pool.map(self.scrape, s)
            pool.close()
            pool.join()
