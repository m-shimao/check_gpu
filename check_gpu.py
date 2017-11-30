# coding: utf-8

import subprocess
import json
from time import sleep
import pprint

DEFAULT_ATTRIBUTES = (
    'index',
    'uuid',
    'name',
    'timestamp',
    'memory.free',
    'memory.used',
    'utilization.gpu',
    'utilization.memory'
)


# nvidia-smiを使って全てのGPUの使用状況を取得
def get_gpu_info(nvidia_smi_path='nvidia-smi', keys=DEFAULT_ATTRIBUTES, no_units=True):
    nu_opt = '' if not no_units else ',nounits'
    cmd = '%s --query-gpu=%s --format=csv,noheader%s' % (nvidia_smi_path, ','.join(keys), nu_opt)
    output = subprocess.check_output(cmd, shell=True)
    lines =str(output).split('\\n')
    lines = [ line.strip() for line in lines if line.strip() != '' ]

    return [ { k: v for k, v in zip(keys, line.split(', ')) } for line in lines ]

# GPUの使用状況をGPU番号を指定して取得
def gpu_is_available(gpu_no):
    usages = get_gpu_info()
    target = usages[gpu_no]
    # GPU使用状況が0で
    if int(target['utilization.gpu']) == 0 and int(target['memory.used']) < 500:
        return True
    return False

# GPU番号を指定してそのGPUが空くまで待つ
def standby(gpu_no, standby_sec = 60 * 10, max_sleep_count = 12):
    n = 0
    while n < max_sleep_count and not gpu_is_available(gpu_no):
        n += 1
        print('standby GPU ...')
        sleep(standby_sec)

    if n == MAX_N:
        print('GPU not available.')
