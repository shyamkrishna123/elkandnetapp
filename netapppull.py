import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import urllib3
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class netapp:
  def netapp(self):
    api_base_url =  "https://192.168.1.35"
    url= api_base_url+'/rest/events?limit=20'
    print(url)
    passw = 'P@ssw0rd123'
    print(passw)
    headers = {
      'Accept' : 'application/vnd.netapp.object.inventory.hal+json',
      'Authorization': 'Basic YWRtaW46UEBzc3cwcmQxMjM='
    }
    mydata = json.dumps({'username':'admin','password':'P@ssw0rd123'})
    s = requests.Session()
    print("-------------s:------------------",s)
    s.auth = ('admin',passw)
    rp = s.post(url=api_base_url,data=mydata,verify=False)
    rs =  s.get(url=url, verify=False,headers=headers)
    print("-------------rs:------------------",rs)
    #result = rs.text
    #print(result.encode('utf8'))
    if rs.status_code == 200:
        dictdump = json.loads(rs.text)
        print("-------------------------------------------------------------------------------------------------------------------")
        print(dictdump)
        print("----------------------------------------------------------")
        sl = dictdump['_embedded'].get('netapp:aggregateInventoryList')
        print(sl)
        for x in sl:
            print(str(x))
            d = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
class elk:
      
  def esconnect(self):
      es_header = [{
        'host': '192.168.1.168',
        'port': '9200'
      }]
      id = 'netapp001'
      try:
        self.esc = Elasticsearch(es_header)
        self.esc.cluster.health(wait_for_status='yellow', request_timeout=2)
        print("successfull")     
      except Exception as ex:
        print("Error connecting es:",ex)
          
  def createindex(self):
      if self.esc.indices.exists(index='netapp-index'):
        print('index already exists')
      else:
            print('creating index')
            self.esc.indices.create(index='netapp-index',ignore=400)
            print('index created')
      #es.indices.create(index='test-index', ignore=400)
      #print(s)

if __name__ == "__main__":
      
  es = elk()
  es.esconnect()
  es.createindex()
  