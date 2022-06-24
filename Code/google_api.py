import pandas as pd
from googleapiclient.discovery import build
from debug import create_log_file


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


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    '''
    Очищаем от лишних символов
    '''
    for i in range(len(data)):
            st = str(data['System'][i])
            st = st.replace('\t', '')
            st = st.replace(' ', '')
            data['System'][i] = st
            st = str(data['Constellation'][i])
            st = st.replace('\t', '')
            st = st.replace(' ', '')
            data['Constellation'][i] = st
            st = str(data['Availability'][i])
            st = st.replace('\t', '')
            st = st.replace(' ', '')
            st = st.replace('y', 'Y')
            st = st.replace('n', 'N')
            data['Availability'][i] = st
    return data


def get_df() -> pd.DataFrame:
    '''
    Делаем запрос в Google API по данным таблицам.
    Вывод:
    - Pandas DF - если не произошло никакой ошибки
    - NoneType - если произошла ошибка
    '''
    try:
        service = build('sheets', 'v4', developerKey=api_key)
        all_systems_df = pd.DataFrame(columns=['System', 'System_id', 'Constellation', 'Availability'])


        def get_df_from_XIX(spreadsheetid, ranges) -> pd.DataFrame:
            request = service.spreadsheets().values().get(spreadsheetId=spreadsheetid, range=ranges)
            response = request.execute()
            df = pd.DataFrame(response['values'][1:], columns=response['values'][0])
            df = df.drop(columns=['Sec Status', 'Ice', 'Dead End', 'Price (Billions)'])
            return df


        def get_df_from_RZR(spreadsheetid, ranges) -> pd.DataFrame:
            request = service.spreadsheets().values().get(spreadsheetId=spreadsheetid, range=ranges)
            response = request.execute()
            df = pd.DataFrame(response['values'][1:], columns=response['values'][0])
            df = df.drop(columns=['Constellation', 'Sec Status', 'Ice Belt', 'Dead End', 'Price (Billions)'])
            df.rename(columns={'Available for rent': 'Availability'}, inplace=True)
            return df


        def get_df_from_Unr(spreadsheetid, ranges) -> pd.DataFrame:
            request = service.spreadsheets().values().get(spreadsheetId=spreadsheetid, range=ranges)
            response = request.execute()
            df = pd.DataFrame(response['values'][1:], columns=response['values'][0])
            df = df.drop(columns=['Constellation', 'Sec Status', 'Sec Class', 'Ice', 'Dead End', 'Price (Billions)'])
            return df


        # Добавляем все в единый ДФ
        for i in range_1:
            all_systems_df = pd.merge(all_systems_df, get_df_from_XIX(spreadsheet_1, i), how="outer")

        all_systems_df = pd.merge(all_systems_df, get_df_from_RZR(spreadsheet_2, range_2), how="outer")

        for i in range_3:
            all_systems_df = pd.merge(all_systems_df, get_df_from_Unr(spreadsheet_3, i), how="outer")

        # Очищаем данные
        all_systems_df = clean_data(all_systems_df)
        all_systems_df.drop_duplicates(keep='first', inplace=True)

        # all_systems_df.to_csv('arenda_table.csv', index=True)

        all_systems_df.index = all_systems_df['System']
        all_systems_df = all_systems_df.drop(columns='System')

    except Exception as err:
        create_log_file(err)
        return None
    else:
        return all_systems_df


# data = get_df()
# print(data.head())
# syst = 'G3D-ZT'
# if all(data.loc[syst, 'Availability'] == 'Yes'):
#     print(True)