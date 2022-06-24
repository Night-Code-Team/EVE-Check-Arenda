from os import system
from types import NoneType
from google_api import get_df
from eve_api import get_system_DF
from debug import create_log_file


system("mode con cols=60 lines=10")


systems_in_renta = get_df()
all_systems = get_system_DF()


def check_system_in_df(syst: str):
    """
    0 - Availability YES
    1 - Not in renta
    2 - Availability NO!!
    3 - System doesn't exist
    """
    if isinstance(systems_in_renta, NoneType):
        return 'Error in Google API! Link to support: err.log'
    if isinstance(systems_in_renta, NoneType):
        return 'Error in EVE API! Link to support: err.log'

    syst = str(syst)
    if any(all_systems['name'].isin([syst])):
        if syst in systems_in_renta.index:
            if systems_in_renta.loc[syst, 'Availability'] == 'Yes':
                return '\033[43m' + 'System is available, but in RENT LIST' + '\033[0m'
            return '\033[41m' + 'System NOT available in RENT LIST' + '\033[0m'
        return '\033[42m' + 'System is NOT in RENT LIST' + '\033[0m'
    return '\033[47m\033[30m' + 'System DOESN\'T EXIST! Check input!' + '\033[0m'


def clear_input(val: str):
    # Очищаем ввод
    try:
        if val[0] == '<':
            b = val.split('<')
            val = b[1].split('>')[1]
        syst = val.upper()
        syst = syst.replace('*', '')
        syst = syst.replace(' ', '')
        return syst
    except IndexError as err:
        print('Wrong input! Check it or link to support: err.log')
        create_log_file(err)


def console_log():
    print(check_system_in_df(clear_input(input())))


if __name__ == '__main__':
    print('All data received.\n\033[42m___Ready___\033[0m')
    while True:
        console_log()