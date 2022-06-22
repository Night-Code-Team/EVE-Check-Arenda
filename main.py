from os import system

import pandas as pd
from googleapiclient.discovery import build


system("mode con cols=60 lines=10")

api_key = 'AIzaSyCeMPfiNLALZHN1Yef7gt1UhBbswpNhCAE'

# Таблица дичей
spreadsheet_1 = '1VYM3xUeOtx0BV831nyeeJFyUWMz5VDfoJIQ3z-35FA4'
# table_1 = "'XIX price list Detorid'!A2:G100"
# table_2 = "'XIX price list Insmother'!A2:G100"
# table_3 = "'Tenerifis'!A2:G100"
# table_4 = "'Immensea'!A2:G100"
# table_5 = "'Wicked creek'!A2:G100"
# table_6 = "'Scalding Pass'!A2:G100"
# table_7 = "'Cache'!A10:G100"        # Снос на 11 строку
# table_8 = "'Feythabolis'!A2:G100"   # Регион не подключен
range_1 = ("'XIX price list Detorid'!A2:G100",
           "'XIX price list Insmother'!A2:G100",
           "'Tenerifis'!A2:G100",
           "'Immensea'!A2:G100",
           "'Wicked creek'!A2:G100",
           "'Scalding Pass'!A2:G100",
           "'Cache'!A10:G100")  # Снос на 11 строку

# Таблица RZR
spreadsheet_2 = '1lGCFgZgrI-phRi8kGUeWki4NqosLDkGo0CDxeIa-1pg'
range_2 = 'A2:100'

# Таблица Unreal
spreadsheet_3 = '1eH3OsJMtCzID7IcYW4EqwvAf9EnnKoX7rgMHO1SF9y0'
# table_1 = "'Wicked Creek'!A2:H100"
# table_2 = "'Omist'!A2:H100"
range_3 = ("'Wicked Creek'!A2:H100", "'Omist'!A2:H100")


def get_df_1(spreadsheetid, ranges):
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheetid, range=ranges)
    response = request.execute()
    df = pd.DataFrame(response['values'], columns=response['values'][0])
    df = df.drop(columns=['Constellation', 'Sec Status', 'Ice', 'Dead End', 'Price (Billions)'])
    return df


def get_df_2(spreadsheetid, ranges):
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheetid, range=ranges)
    response = request.execute()
    df = pd.DataFrame(response['values'], columns=response['values'][0])
    df = df.drop(columns=['Constellation', 'Sec Status', 'Ice Belt', 'Dead End', 'Price (Billions)'])
    df.rename(columns={'Available for rent': 'Availability'}, inplace=True)
    return df


def get_df_3(spreadsheetid, ranges):
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheetid, range=ranges)
    response = request.execute()
    df = pd.DataFrame(response['values'], columns=response['values'][0])
    df = df.drop(columns=['Constellation', 'Sec Status', 'Sec Class', 'Ice', 'Dead End', 'Price (Billions)'])
    return df


service = build('sheets', 'v4', developerKey=api_key)

df1 = get_df_1(spreadsheet_1, range_1[0])
all_systems_df = df1

for i in range(1, len(range_1)):
    df1 = get_df_1(spreadsheet_1, range_1[i])
    all_systems_df = pd.merge(all_systems_df, df1, how="outer")

df2 = get_df_2(spreadsheet_2, range_2)
all_systems_df = pd.merge(all_systems_df, df2, how="outer")

for i in range_3:
    df3 = get_df_3(spreadsheet_3, i)
    all_systems_df = pd.merge(all_systems_df, df3, how="outer")

for i in range(len(all_systems_df['System'])):
    st = str(all_systems_df['System'][i])
    all_systems_df['System'][i] = st.replace('\t', '')

all_systems_df.index = all_systems_df['System']
all_systems_df = all_systems_df.drop(columns='System')


def check_system_in_df(syst: str):
    """
    0 - Availability YES
    1 - Not in renta
    2 - Availability NO!!
    """
    if syst in all_systems_df.index:
        if all_systems_df.loc[syst, 'Availability'] == 'Yes':
            return '\033[43m' + 'System is available, but in RENT LIST' + '\033[0m'
        return '\033[41m' + 'System NOT available in RENT LIST' + '\033[0m'
    return '\033[42m' + 'System is NOT in RENT LIST' + '\033[0m'


def clear_system(val: str):
    syst = val.upper()
    syst = syst.replace('*', '')
    return syst


def console_log():
    print(check_system_in_df(clear_system(input())))


if __name__ == '__main__':
    while True:
        console_log()
