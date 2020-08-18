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

def calculate_average(scores):
  score_average_raw = numpy.average(scores)
  average_scores = {}
  average_scores['main'] = Decimal(str(score_average_raw)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
  average_scores['max'] = numpy.amax(scores)
  average_scores['min'] = numpy.amin(scores)

  return average_scores

def measure(device):
  device_name = {
    'mobile': 'モバイル',
    'desktop': 'パソコン'
  }

  print(f'[ {device_name[device]} ]')

  payload['strategy'] = device
  url_name = api_url + "?url=" + url

  scores = []
  field_fcp_scores = []
  field_lcp_scores = []
  field_fid_scores = []
  field_cls_scores = []
  lab_cls_scores = []

  for i in range(measurement_count):
    result = requests.get(url_name, params = payload)
    result_json = result.json()
    result_score = result_json['lighthouseResult']['categories']['performance']['score']
    displayed_score = math.floor(result_score * 100)

    field_data_scores = {}
    field_data_scores['fcp'] = \
      result_json['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['percentile'] / 1000
    field_data_scores['lcp'] = \
      result_json['loadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['percentile'] / 1000
    field_data_scores['fid'] = \
      result_json['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['percentile']
    field_data_scores['cls'] = \
      result_json['loadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE']['percentile']

    lab_data_scores = {}
    lab_data_scores['cls'] = result_json['lighthouseResult']['audits']['cumulative-layout-shift']['numericValue']

    field_fcp_scores.append(field_data_scores['fcp'])
    field_lcp_scores.append(field_data_scores['lcp'])
    field_fid_scores.append(field_data_scores['fid'])
    field_cls_scores.append(field_data_scores['cls'])
    lab_cls_scores.append(lab_data_scores['cls'])
    scores.append(displayed_score)
    print(displayed_score, end=' ')

  average_scores = calculate_average(scores)
  average_field_fcp_scores = calculate_average(field_fcp_scores)
  average_field_lcp_scores = calculate_average(field_lcp_scores)
  average_field_fid_scores = calculate_average(field_fid_scores)
  average_field_cls_scores = calculate_average(field_cls_scores)
  average_lab_cls_scores = calculate_average(lab_cls_scores)
  print('\n平均 {main} 点（最低 {min} 点、最高 {max} 点）' \
    .format(
      main=average_scores['main'],
      min=average_scores['min'],
      max=average_scores['max']
    ))
  print('(フィールドデータ)', end=' ')
  print('FCP: 平均 {main} s'.format(main=average_field_fcp_scores['main']), end=', ')
  print('LCP: 平均 {main} s'.format(main=average_field_lcp_scores['main']), end=', ')
  print('FID: 平均 {main} ms'.format(main=average_field_fid_scores['main']), end=', ')
  print('CLS: 平均 {main}'.format(main=average_field_cls_scores['main']))
  print('(ラボデータ)', end=' ')
  print('累積レイアウト変更: 平均 {main}'.format(main=average_lab_cls_scores['main']))

print('\n'.join(map(str, url_list)))
print(f'を測定中...({measurement_count}回計測)')

for i, url in enumerate(url_list):
  print(f'\n({i + 1}/{len(url_list)}) {url}')

  measure('mobile')
  measure('desktop')

  print('\n' + '=' * 60)

print('\n測定完了！')
