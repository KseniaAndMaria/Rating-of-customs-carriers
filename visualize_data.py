import re
import json
import functools
import pandas as pd
from os import listdir, path
from constants import Constants
import matplotlib.pyplot as plt

ooo_regex = re.compile(r"общество с ограниченной ответственностью", re.IGNORECASE)
zao_regex = re.compile(r'закрытое акционерное общество', re.IGNORECASE)
ao_regex = re.compile(r'акционерное общество', re.IGNORECASE)

def visualize_data():
  def collect_data():
    suppliers = []
    carrier_info_folder = path.join(Constants.data_folder, Constants.carrier_info_folder)

    filelist = list(filter(lambda filename: filename.endswith('.json'), listdir(carrier_info_folder)))

    for filename in filelist:
      data = json.load(open(path.join(carrier_info_folder, filename), 'r'))['suppliers']['data'][0]

      contract44 = data.get('contractsYearStats', { Constants.selected_year: { 'contractsCount': 0, 'contractsSum': 0 } })[Constants.selected_year]
      contract223 = data.get('contracts223YearStats', { Constants.selected_year: { 'contractsCount': 0, 'contractsSum': 0 } })[Constants.selected_year]

      shortly_name = functools.reduce(lambda lastName, currentName: currentName if len(lastName) > len(currentName) else lastName, data['allNames'])
      shortly_name = re.sub(ooo_regex, 'OOO', shortly_name)
      shortly_name = re.sub(zao_regex, 'ЗАО', shortly_name)
      shortly_name = re.sub(ao_regex, 'OOO', shortly_name)

      supplier = {
        'organization_name': shortly_name,
        '44_fz_count': contract44['contractsCount'],
        '44_fz_sum': contract44['contractsSum'] / 1000,
        '223_fz_count': contract223['contractsCount'],
        '223_fz_sum': contract223['contractsSum'] / 1000,
      }

      suppliers.append(supplier)

    return suppliers

  def draw_first_plot(data):
    data = data[data['44_fz_sum'] > 0]
    data = data.sort_values(by=['44_fz_sum'], ascending=False)
    data = data.reset_index()
    data.plot(use_index=True, y='44_fz_sum', label='Выручка по контрактам', rot=90)
    plt.xticks(data.index, data['organization_name'])
    plt.title('Лидеры по объемам выручки с госконтрактов за ' + Constants.selected_year + ' год. Контракты оформленные по 44 ФЗ')
    plt.xlabel('Название организации')
    plt.ylabel('Объем выполненных контрактов (тыс. руб.)')
    plt.subplots_adjust(bottom=0.5)
    plt.gca().set_yscale("log")
    plt.grid()
    plt.show()

  def draw_second_plot(data):
    data = data[data['44_fz_count'] > 0]
    data = data.sort_values(by=['44_fz_count'], ascending=False)
    data = data.reset_index()
    data.plot(use_index=True, y='44_fz_count', label='Количество выполненных контрактов', rot=90)
    plt.xticks(data.index, data['organization_name'])
    plt.title('Лидеры по объемам выполненных госконтрактов за ' + Constants.selected_year + ' год. Контракты оформленные по 44 ФЗ')
    plt.xlabel('Название организации')
    plt.ylabel('Количество выполненных контрактов (шт.)')
    plt.subplots_adjust(bottom=0.5)
    plt.gca().set_yscale("log")
    plt.grid()
    plt.show()

  def draw_third_plot(data):
    data = data[data['223_fz_sum'] > 0]
    data = data.sort_values(by=['223_fz_sum'], ascending=False)
    data = data.reset_index()
    data.plot(use_index=True, y='223_fz_sum', label='Выручка по контрактам', rot=90)
    plt.xticks(data.index, data['organization_name'])
    plt.title('Лидеры по объемам госконтрактов за ' + Constants.selected_year + ' год. Контракты оформленные по 223 ФЗ')
    plt.xlabel('Название организации')
    plt.ylabel('Объем выполненных контрактов (тыс. руб.)')
    plt.subplots_adjust(bottom=0.5)
    plt.gca().set_yscale("log")
    plt.grid()
    plt.show()

  def draw_forth_plot(data):
    data = data[data['223_fz_count'] > 0]
    data = data.sort_values(by=['223_fz_count'], ascending=False)
    data = data.reset_index()
    data.plot(use_index=True, y='223_fz_count', label='Количество выполненных контрактов', rot=90)
    plt.xticks(data.index, data['organization_name'])
    plt.title('Лидеры по объемам выполненных госконтрактов за ' + Constants.selected_year + ' год. Контракты оформленные по 223 ФЗ')
    plt.xlabel('Название организации')
    plt.ylabel('Количество выполненных контрактов (шт.)')
    plt.subplots_adjust(bottom=0.5)
    plt.gca().set_yscale("log")
    plt.grid()
    plt.show()

  print('Visualizing...')

  data = pd.DataFrame(collect_data())

  draw_first_plot(data.copy())
  draw_second_plot(data.copy())
  draw_third_plot(data.copy())
  draw_forth_plot(data.copy())
