import requests
import datetime as dt
from urllib3.exceptions import HTTPError
import json
import re
import itertools


def range_dates(start:dt.date|str, stop:dt.date|str):
    if not isinstance(start, dt.date):
        start = dt.date.fromisoformat(start)
    if not isinstance(stop, dt.date):
        stop = dt.date.fromisoformat(stop)
    ONE_DAY = dt.timedelta(days=1)

    date = start
    while date < stop:
        if date.day == 1:
            print(date)
        yield date.isoformat()
        date += ONE_DAY


def download(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content.decode(encoding='utf-8')
    else:
        response.raise_for_status()

def parseData(html:str):
    ret = {}
    missing = []
    SPAN = r'(?:\s*<span>.*?<\/span>)?'
    for tag, tag_json in (
        ('Temperatura mitjana', 'temperatura-avg'),
        ('Temperatura màxima', 'temperatura-max'),
        ('Temperatura mínima', 'temperatura-min'),
        ('Humitat relativa mitjana', 'humitat-avg'),
        ('Precipitació acumulada', 'precipitacio-acumulada'),
        ('Ratxa màxima del vent', 'vent-max'),
        ('Pressió atmosfèrica mitjana', 'pressio-atmosferica-avg'),
        ('Irradiació solar global', 'irradiacio-solar-global'),
    ):
        data = None
        regex = r'<tr>\s*<th.*?>\s*'+tag+SPAN+r'\s*<\/th>\s*<td.*?>(.*?)<\/td>'
        m1 = re.search(regex, html, flags=re.MULTILINE|re.DOTALL)
        if m1:
            m2 = re.search(r'(- *)?[0-9]+(\.[0-9]+)?', m1.group(1),  flags=re.MULTILINE|re.DOTALL)
            if m2:
                data = float(m2.group(0).replace(' ', ''))  
        if data is not None:
            ret[tag_json] = data
        else:
            missing.append(tag)
    for tag in ('TemperaturaHumitat', 'VelocitatDireccioVent', 'Precipitacio'):
        regex = r'Meteocat\.grafiquesEstacions\.renderitzarGrafica' + tag + r'\(\s*(\{.*?\})'
        m = re.search(regex, html, flags=re.MULTILINE|re.DOTALL)
        if m:
            data = re.sub(r'//.*', '', m.group(1))
            data = data.replace("'", '"')
            data = json.loads(data)
            ret.update(data)
        else:
            missing.append(tag)
    return json.dumps(ret), missing



def getMeteoData(date:str):
    url = f'https://www.meteo.cat/observacions/xema/dades?codi=D5&dia={date}T00:00Z'
    out, err = None, None
    try:
        html = download(url)
    except HTTPError as e:
        err = f'HTTPError: {e}'
        return out, err
    
    try:
        out, err = parseData(html)
        if err:
            err = 'MissingData: '+', '.join(err)
    except Exception as e:
        err = f'ParseError: {e}'
    if err:
        with open(f'data/meteocat/raw-data/{date}.html', 'w', encoding='utf-8') as file:
            file.write(html)
    return out, err

if __name__ == '__main__':
    with open('data/meteocat/data.dat', 'a', encoding='utf-8') as output:
        with open('data/meteocat/errors.out', 'a', encoding='utf-8') as errors:
            #for date in range_dates('2009-06-01', dt.date.today()):
            for date in itertools.chain(
               ['2011-01-29', '2011-01-30', '2016-09-24', '2016-09-25', '2016-09-26', '2016-09-27'],
               range_dates('2020-07-10', dt.date.today())
            ):
                out, err = getMeteoData(date)
                if out:
                    output.write(f'{date};{out}\n')
                if err:
                    errors.write(f'{date};{err}\n')
                    errors.flush()