
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import urllib3
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class covid:
      
      def __init__(self):
            self.api_base_url =  "https://192.168.1.35"
            self.url= "https://coronavirus-monitor.p.rapidapi.com/coronavirus/latest_stat_by_country.php"
            self.querystring = {"country":"india"}
            print(self.url)
            self.headers = {
               'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
                'x-rapidapi-key': "1fc6475116mshc24dbab8932c716p15f0e7jsn781836e6aea0"
            }
            
      def netappconnect(self):
          response = requests.request("GET", self.url, headers=self.headers,params=self.querystring)
          data = json.loads(response.text)
          # print(response.text)
          return data
class elk:
      
      
  def __init__(self):
      self.es_header = [{
        'host': '192.168.1.168',
        'port': '9200'
      }]
      self.index = 'covid'
      self.datawithtime = {}
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
     
      self.datawithtime = {"data": data,"timestamp": datetime.now()}
      self.esc.index(index=self.index,doc_type='events',body=datawithtime)
      print("data posting completed")
def main():
      es = elk()
      es.createindex()
      ntapp = covid()
      data = ntapp.netappconnect()
      print(data)
      es.putdata(data)

if __name__ == "__main__":
      main()
      
  
  