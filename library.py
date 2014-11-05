# -*- coding: utf-8 -*-

from requests import session, codes
from BeautifulSoup import BeautifulStoneSoup

SITE_URL = 'http://szkolenie.bg.pg.gda.pl/'

# NALEŻY PISAĆ WIELKIMI LITERAMI

payload = {
    'imie': 'IMIĘ',
    'nazwisko': 'NAZWISKO',
    'nr_albumu': 155000,
    'zaloguj': ''
}

with session() as c:
    request = c.post(SITE_URL, data=payload)
    soup = BeautifulStoneSoup(request.text)
    del payload['zaloguj']
    for buttons in soup.findAll('button'):
        if buttons.get('name') == 'id_test': # To jest jeden z testów
            payload['id_test'] = buttons.get('value')
            # Pobranie pytań
            request = c.post(SITE_URL, data=payload)
            # Zmienne pomocnicze
            test = BeautifulStoneSoup(request.text)
            last_name = ''
            max_val = 0
            payload_test = {}
            # Przetwarzanie kolejnych pytań
            for radio_inputs in test.findAll('input', {'type': 'radio'}):
                # Nie przetwarzamy wielokrotnie tego samego pytania
                if radio_inputs.get('name') == last_name:
                    continue
                if last_name != '':
                    payload_test[last_name] = max_val
                last_name = radio_inputs.get('name')
                max_val = int(radio_inputs.get('value'))
                # Szukanie odpowiedzi na pytanie o największej wartości
                for input in test.findAll('input', {'name': last_name}):
                    # czy to jest najmniejsza wartość odpowiedzi?
                    if int(input.get('value')) <= max_val:
                        max_val = int(input.get('value'))
            # Uzupełnienie dla ostatniego formularza
            payload_test[last_name] = max_val
            # Uzupełnienie payload'u odpowienimi danymi
            payload_test['sprawdz'] = 'Wyślij'
            payload_test.update(payload)
            # Zapis wyników
            if c.post(SITE_URL, data=payload_test).status_code == codes.ok:
                print '[INFO] Test rozwiazany'
            else:
                print '[ERROR] Blad podczas rozwiazywania testu'
        else: # nie jest ID testu to nas nie obchodzi → nie ten przycisk
            pass
    print '[INFO] Wszystkie testy rozwiazane'
