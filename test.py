import requests
import urllib3
import json
urllib3.disable_warnings()
headers = {
              'Authorization': 'Basic YWRtaW46UEBzc3cwcmQxMjM='}
s = requests.Session()
rs =  s.get(url='https://192.168.1.35/rest/clusters/1/aggregates?sort=iops~dsc', verify=False,headers=headers)
print(rs)
if rs.status_code == 200:
 	dictdump = json.loads(rs.text)
	print(dictdump)
