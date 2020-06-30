import config
import requests
import math
import numpy
from decimal import Decimal, ROUND_HALF_UP

# 測定回数
measurement_count = 3;

# 測定対象 URL
url_list = [
  'https://www.google.com/',
  'https://www.yahoo.co.jp/',
  'https://www.bing.com/'
]

api_url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
api_key = config.API_KEY

payload = { 'key': api_key }

def measure(device):
  device_name = {
    'mobile': 'モバイル',
    'desktop': 'パソコン'
  }

  print(f'[ {device_name[device]} ]')

  payload['strategy'] = device
  url_name = api_url + "?url=" + url

  scores = []

  for i in range(measurement_count):
    result = requests.get(url_name, params = payload)
    result_json = result.json()
    result_score = result_json['lighthouseResult']['categories']['performance']['score']
    displayed_score = math.floor(result_score * 100)

    scores.append(displayed_score)
    print(displayed_score, end=' ')

  score_average_raw = numpy.average(scores)
  score_average = Decimal(str(score_average_raw)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
  score_max = numpy.amax(scores)
  score_min = numpy.amin(scores)
  print(f'\n平均 {score_average} 点（最低 {score_min} 点、最高 {score_max} 点）')

print('\n'.join(map(str, url_list)))
print(f'を測定中...({measurement_count}回計測)')

for i, url in enumerate(url_list):
  print(f'\n({i + 1}/{len(url_list)}) {url}')

  measure('mobile')
  measure('desktop')

  print('\n' + '=' * 60)

print('\n測定完了！')
