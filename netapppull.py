import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import urllib3
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class netapp:
      
      def __init__(self):
            self.api_base_url =  "https://192.168.1.35"
            self.url= self.api_base_url+'/rest/events'
            print(self.url)
            self.headers = {
              'Accept' : 'application/vnd.netapp.object.inventory.hal+json',
              'Authorization': 'Basic YWRtaW46UEBzc3cwcmQxMjM='
            }
            
      def netappconnect(self):
            s = requests.Session()
            rs =  s.get(url=self.url, verify=False,headers=self.headers)
            if rs.status_code == 200:
                self.dictdump = json.loads(rs.text)
                #print(self.dictdump)
                print("-------------------------------------------------------------------------------------------------------------------")
                print("----------------------------------------------------------")
                sl = self.dictdump['_embedded'].get('netapp:aggregateInventoryList')
                print(sl)
                return self.dictdump
                
class elk:
      
      
  def __init__(self):
      self.es_header = [{
        'host': '192.168.1.168',
        'port': '9200'
      }]
      self.id = 'netapp001'
      self.index = 'netapp-index'
  def esconnect(self):
      try:
        self.esc = Elasticsearch(self.es_header)
        self.esc.cluster.health(wait_for_status='yellow', request_timeout=2)
        print("successfull")     
      except Exception as ex:
        print("Error connecting es:",ex)
          
  def createindex(self):
      self.esconnect()
      if self.esc.indices.exists(index=self.index):
        print('index already exists')
      else:
            print('creating index')
            self.esc.indices.create(self.index,ignore=400)
            print('index created')
      #es.indices.create(index='test-index', ignore=400)
      #print(s)
  def putdata(self,data):
        self.esc.index(index=self.index,doc_type='events',body=data)
        print("data posting completed")
def main():
      es = elk()
      es.createindex()
      ntapp = netapp()
      data = ntapp.netappconnect()
      es.putdata(data)

if __name__ == "__main__":
      main()
      
  
  