# check_gpu
This is Python script. You can check gpu usage and standby until avalable.

## Usage
```
import check_gpu

# require
gpu_no = 1
# default 10 min
sleep_sec = 60 * 10
# default 12 
max_sleep_count = 12

check_gpu.standby(gpu_no, sleep_sec, max_sleep_count)
```
