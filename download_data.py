import csv
import json
import urllib.request as request
from constants import Constants
from os import mkdir, path
from time import sleep

def download_data():
  if not path.exists('network_error_cache.json'):
    file = open('network_error_cache.json', 'w')
    json.dump([], file)
    file.close()

  network_error_cache = json.load(open('network_error_cache.json', 'r'))

  data_folder = Constants.data_folder
  carriers_filename = path.join(Constants.data_folder, Constants.carriers_filename)

  def download_datasets():
    if not path.exists(data_folder):
      mkdir(Constants.data_folder)

    with open(carriers_filename, 'wb') as carriers_file:
      carriers_dataset = request.urlopen(Constants.carriers_dataset_url).read()
      carriers_file.write(carriers_dataset)

  def download_carrier_info(inn, kpp):
    info_folder = path.join(Constants.data_folder, Constants.carrier_info_folder)
    carrier_info_path = path.join(info_folder, inn + '.json')

    if not path.exists(info_folder):
      mkdir(info_folder)

    if path.exists(carrier_info_path) or (str(inn) + str(kpp) in network_error_cache):
      return

    carrier_info = None

    try:
      carrier_info = request.urlopen(Constants.carrier_info_base_url + '?inn=' + inn + '&kpp=' + kpp).read()

      if carrier_info == '':
        return
    except Exception:
      network_error_cache.append(str(inn) + str(kpp))
      return

    with open(carrier_info_path, 'wb') as carrier_info_file:
      carrier_info_file.write(carrier_info)
    
    sleep(Constants.timeout)

  print('Datasets downloading...')

  download_datasets()

  carriers_file = open(carriers_filename, 'r')
  carriers_reader = csv.reader(carriers_file, delimiter=';')

  next(carriers_reader) # skiping header

  for carrier in carriers_reader:
    inn = carrier[18]
    kpp = carrier[19]

    if (len(inn) == 10 or len(inn) == 12) and len(kpp) == 9:
      download_carrier_info(inn, kpp)

  json.dump(network_error_cache, open('network_error_cache.json', 'w'))
