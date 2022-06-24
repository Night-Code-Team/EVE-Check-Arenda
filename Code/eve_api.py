import requests
import pandas as pd
from debug import create_log_file


all_regions_url = 'https://esi.evetech.net/latest/universe/regions/?datasource=tranquility'
info_about_regions_url = 'https://esi.evetech.net/latest/universe/regions/{}/?datasource=tranquility'

info_about_constellations_url = 'https://esi.evetech.net/latest/universe/constellations/{}/?datasource=tranquility'

all_systems_id_url = 'https://esi.evetech.net/latest/universe/systems/?datasource=tranquility'
info_about_sys_url = 'https://esi.evetech.net/latest/universe/systems/{}/?datasource=tranquility'


def get_json_res(resp: str):
    return requests.get(resp).json()


def get_info_about_system(system_id: str):
    return get_json_res(f'https://esi.evetech.net/latest/universe/systems/{system_id}/?datasource=tranquility')


def get_info_about_region(region_id: str):
    return get_json_res(f'https://esi.evetech.net/latest/universe/regions/{region_id}/?datasource=tranquility')


def get_info_about_constellation(constellation_id: str):
    return get_json_res(f'https://esi.evetech.net/latest/universe/constellations/{constellation_id}/?datasource=tranquility')


def get_all_regions() -> pd.DataFrame:
    all_regions_id = get_json_res(all_regions_url)
    data = pd.DataFrame(columns=['name', 'region_id', 'constellations'])
    for i in all_regions_id:
        region_info = get_info_about_region(str(i))
        try:
            data.loc[len(data.index)] = [region_info['name'], region_info['region_id'], region_info['constellations']]
            print('Data from region {} received'.format(region_info['name']))
        except KeyError as err:
            print('Exeption!', err)
            continue
    # Сохраняем файл
    data.to_csv('region_id.csv', index=False)
    return data


def get_constellation_in_regions(regions_ids: list):
    data = pd.DataFrame(columns=['name', 'constellation_id', 'systems', 'position', 'region_id', 'region'])
    for region_id in regions_ids:
        constellations = get_info_about_region(str(region_id))['constellations']
        for i in constellations:
            constellation_info = get_info_about_constellation(str(i))
            try:
                data.loc[len(data.index)] = [constellation_info['name'], constellation_info['constellation_id'], constellation_info['systems'], constellation_info['position'], constellation_info['region_id'], get_info_about_region(constellation_info['region_id'])['name']]
                print('Data for constellation {} received'.format(constellation_info['name']))
            except KeyError as err:
                print('Exeption!', err)
                continue
    # Сохраняем файл
    data.to_csv('constellation_id.csv', index=False)
    return data


def get_system_in_constellation(constellations_ids: list):
    data = pd.DataFrame(columns=['name', 'system_id', 'security_status', 'position', 'constellation_id', 'constellation'])
    for constellation_id in constellations_ids:
        systems = get_info_about_constellation(str(constellation_id))['systems']
        for i in systems:
            system_info = get_info_about_system(str(i))
            try:
                data.loc[len(data.index)] = [system_info['name'], system_info['system_id'], system_info['security_status'], system_info['position'], system_info['constellation_id'], get_info_about_constellation(system_info['constellation_id'])['name']]
                print('Data for system {} received'.format(system_info['name']))
            except KeyError as err:
                print('Exeption!', err)
                continue
    # Сохраняем файл
    data.to_csv('system_id.csv', index=False)
    return data


# test = pd.read_csv('constellation_id.csv')
# list_of_systems = []
# for i in test['systems']:
#     a = i
#     a = a.replace(',', '')
#     a = a.replace('[', '')
#     a = a.replace(']', '')
#     a = a.split(' ')
#     for j in a:
#         list_of_systems.append(j)

# list_of_constellations = []
# for i in test['constellation_id']:
#     list_of_constellations.append(i)
# 
# get_system_in_constellation(list_of_constellations)


# print(list_of_systems)
# Insmother      10000009
# Scalding Pass  10000008
# Wicked Creek   10000006
# Detorid        10000005
# Immensea       10000025
# Tenerifis      10000061


def get_system_DF() -> pd.DataFrame:
    '''
    Возвращает DF со всеми подключенными системами.
    - Если файл не найден, возвращаяется None
    '''
    try:
        data = pd.read_csv('system_id.csv')
    except Exception as err:
        create_log_file(err)
        return None
    else:
        return data
