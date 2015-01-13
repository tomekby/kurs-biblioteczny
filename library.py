# -*- coding: utf-8 -*-

from requests import session, codes
from bs4 import BeautifulSoup

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
    soup = BeautifulSoup(request.text)
    del payload['zaloguj']
    for buttons in soup.findAll('button'):
        if buttons.get('name') == 'id_test': # To jest jeden z testów
            payload['id_test'] = buttons.get('value')
            # Pobranie pytań
            request = c.post(SITE_URL, data=payload)
            # Zmienne pomocnicze
            test = BeautifulSoup(request.text)
            last_input_name = ''
            correct_answer = 0
            payload_test = {}
            # Przetwarzanie kolejnych pytań
            for radio_inputs in test.findAll('input', {'type': 'radio'}):
                # Nie przetwarzamy wielokrotnie tego samego pytania
                if radio_inputs.get('name') == last_input_name:
                    continue
                if last_input_name != '':
                    payload_test[last_input_name] = correct_answer
                last_input_name = radio_inputs.get('name')
                correct_answer = int(radio_inputs.get('value'))
                # Szukanie odpowiedzi na pytanie o największej wartości
                for input in test.findAll('input', {'name': last_input_name}):
                    # czy to jest najmniejsza wartość odpowiedzi?
                    if int(input.get('value')) <= correct_answer:
                        correct_answer = int(input.get('value'))
            # Uzupełnienie dla ostatniego formularza
            payload_test[last_input_name] = correct_answer
            # Uzupełnienie payload'u odpowienimi danymi
            payload_test['sprawdz'] = 'Wyślij'
            payload_test.update(payload)
            # Zapis wyników
            if c.post(SITE_URL, data=payload_test).status_code == codes.ok:
                print('[INFO] Test rozwiazany')
            else:
                print('[ERROR] Blad podczas rozwiazywania testu')
        else: # nie jest ID testu to nas nie obchodzi → nie ten przycisk
            pass
    print('[INFO] Wszystkie testy rozwiazane')
