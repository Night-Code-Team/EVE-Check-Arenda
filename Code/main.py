from os import system
from types import NoneType
from google_api import get_google_df
from eve_api import get_system_DF
from debug import create_log_file
from pandas import DataFrame

import re
import eel


err = False


system("mode con cols=60 lines=10")

print('Please wait, I\'m request data from Google and EVE API...')

# Get Google data
systems_in_renta = get_google_df()
if isinstance(systems_in_renta, DataFrame):
    print('Data from Google   \033[42m\033[30mRECEIVED\033[0m')
else:
    print('Data from Google   \033[41m\033[30mError\033[0m')
    err = True


# Get EVE data
all_systems = get_system_DF()
if isinstance(all_systems, DataFrame):
    print('Data from EVE      \033[42m\033[30mRECEIVED\033[0m')
else:
    print('Data from EVE      \033[41m\033[30mError\033[0m')
    err = True



def check_system_in_df(syst: str):
    if isinstance(systems_in_renta, NoneType):
        return 'Error in Google API! Link to support: err.log'
    if isinstance(systems_in_renta, NoneType):
        return 'Error in EVE API! Link to support: err.log'

    syst = str(syst)
    if any(all_systems['name'].isin([syst])):
        if syst in systems_in_renta.index:
            if systems_in_renta.loc[syst, 'Availability'] == 'Yes':
                return f'\033[43m\033[30m' + 'System ' + syst + ' is available, but in RENT LIST' + '\033[0m'
            return f'\033[41m\033[30m' + 'System ' + syst + ' NOT available in RENT LIST' + '\033[0m'
        return f'\033[42m\033[30m' + 'System ' + syst + ' is NOT in RENT LIST' + '\033[0m'
    return f'\033[47m\033[30m\033[30m' + 'System ' + syst + ' DOESN\'T EXIST! Check input!' + '\033[0m'


def clear_input(val: str):
    # Очищаем ввод
    if val[0] == '<':
        try:
            b = val.split('<')
            val = b[1].split('>')[1]
        except Exception:
            print('Wrong input!')
    try:
        syst = val.upper()
        syst = syst.replace('*', '')
        syst = syst.replace(' ', '')
    except:
        print('Wrong input!')
    return syst



def clear_input_regular(val: str) -> str():
    reqular = r"[0-9A-Z][0-9A-Z\-][0-9A-Z\-][0-9A-Z\-][0-9A-Z\-][0-9A-Z]" # https://regex101.com/r/F8dY80/3
    val = val.upper()
    val = val.replace('*', '')
    val = val.replace(' ', '')
    exp = str(re.search(reqular, val))
    return exp


def console_log():
    print(check_system_in_df(clear_input(input())))


if __name__ == '__main__':
    if err:
        print('Something went wrong, link error.log file to support')
    else:
        print('All data received! \033[42m\033[30mREADY\033[0m')
    while True:
        console_log()
