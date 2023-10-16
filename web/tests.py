# import time
# from tqdm import tqdm
#
# wait_time = 100
#
# prefix = "等待中。。。"
#
# for i in tqdm(range(wait_time),unit="秒",unit_scale=True,desc=prefix):
#     time.sleep(1)


form = "xx"
v1 = "non_field_errors.xxxx"
data_list = v1.split(".")
for name in data_list:
    data = getattr(form,name)
    if callable(data):
        form = data()
    else:
        form = data