import requests
import hashlib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import urllib3
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class netapp:
      
      def __init__(self,api_name):
            self.api_base_url =  "https://192.168.1.35"
            self.url= self.api_base_url+'/rest/'+api_name
            print(self.url)
            self.headers = {
              'Accept' : 'application/vnd.netapp.object.inventory.hal+json',
              'Authorization': 'Basic YWRtaW46UEBzc3cwcmQxMjM='
            }
            self.clusterheaders = {
              'Authorization': 'Basic YWRtaW46UEBzc3cwcmQxMjM='
            }
            
      def netappconnect(self,headers):
            s = requests.Session()
            rs =  s.get(url=self.url, verify=False,headers=headers)
            if rs.status_code == 200:
                self.dictdump = json.loads(rs.text)
                #print(self.dictdump)
                print("-------------------------------------------------------------------------------------------------------------------")
                print("----------------------------------------------------------")
                return self.dictdump
                
class elk:
      
      
  def __init__(self):
      self.es_header = [{
        'host': '192.168.1.168',
        'port': '9200'
      }]
      self.id = 'netapp001'
      self.index = 'netapp-index'
      self.datawithtime = {}

  def esconnect(self):
      try:
        self.esc = Elasticsearch(self.es_header)
        self.esc.cluster.health(wait_for_status='yellow', request_timeout=2)
        print("successfull")     
      except Exception as ex:
        print("Error connecting es:",ex)
          
  def createindex(self,index):
      self.esconnect()
      if self.esc.indices.exists(index=index):
        print('index already exists')
      else:
            print('creating index')
            self.esc.indices.create(index,ignore=400)
            print('index created')
      #es.indices.create(index='test-index', ignore=400)
      #print(s)
  
  def hash(self,hash):
            hash.pop('triggeredDuration',None)
            hash.pop('obsoleteDuration',None)
            embdata = json.dumps(hash)
            #print(embdata)
            hash = hashlib.md5(embdata.encode("utf-8")).hexdigest()
            print(hash)
            hash = str(hash)
            print(hash)
            return hash
  
  def ifexist(self,hash):
      try:
            res =  self.esc.search(index="hash-index", doc_type='hash',body={
            "query": {
              "bool" : {
               "must" : {
                 "term" : { "data" : hash }
            }}}})

            res = res['hits']['hits']
            if res:
                  return True
            else:
                  return False
      except Exception as ex:
            print(ex)
       
  def putdata(self,data,type,index,api_name):
      date =  datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
      #print(date)
      #print("------------------------------------------------------------------")
      #self.esc.index(index=self.index,doc_type='date',body=x)
      self.datawithtime = {"@timestamp":date,"data": data,"type":api_name}      
      #print("------------------------------------------------------------------")
      print(self.datawithtime)
      self.esc.index(index=index,doc_type=type,body=self.datawithtime)
      print("data posting completed")           

  def update(self,embdata,api_name):
      for x in embdata:
            hash = self.hash(x)
            
            if self.ifexist(hash):
                  print("already exist")
            else:
                  print("------------------------------------------------------------------")
                  print("not presnt")
                  print("------------------------------------------------------------------")
                  print(x)
                  print("------------------------------------------------------------------")
                  self.putdata(hash,'hash','hash-index',api_name)
                  self.putdata(x,'events','netapp-index',api_name)
class logger:
      def __init__(self):
            self.es = elk()
            self.es.createindex('netapp-index')
            self.es.createindex('hash-index')
    
      def logger(self,api_name,namespace_value=None):
            ntapp = netapp(api_name)
            if namespace_value is not None:
                  print("not none")
                  data = ntapp.netappconnect(ntapp.headers)
                  embdata = data['_embedded'].get(namespace_value)
                  self.es.update(embdata,api_name)
                  if api_name == 'clusters':
                        return embdata
                  else:
                        print("not required")
            else:
                  print("clusetr id")
                  data = ntapp.netappconnect(ntapp.clusterheaders)
                  print("*******DATA*********")
                  self.es.update(data,api_name)
            
def main():
      log = logger()
      print("------------------------------------------------------------------")
      print("events")
      log.logger('events','netapp:eventDtoList')
      print("------------------------------------------------------------------")
      print("ports")
      log.logger('ports','netapp:portInventoryList')
      print("------------------------------------------------------------------")
      print("Nodes")
      log.logger('nodes','netapp:nodeInventoryList')
      print("------------------------------------------------------------------")
      print("svms")
      log.logger('svms','netapp:svmInventoryList')
      print("------------------------------------------------------------------")
      print("clusters")
      res = log.logger('clusters','netapp:clusterInventoryList')
      for x in res:
            id = x['cluster'].get('id')
            id = str(id)
            print(id)
            log.logger('clusters/'+id+'/aggregates?dateTimeRange=LAST_1h&sort=iops~dsc')
            log.logger('clusters/'+id+'/luns?dateTimeRange=LAST_1h&sort=iops~dsc')
            log.logger('clusters/'+id+'/nodes?dateTimeRange=LAST_1h&sort=iops~dsc')
            log.logger('clusters/'+id+'/svms?dateTimeRange=LAST_1h&sort=iops~dsc')
            log.logger('clusters/'+id+'/volumes?dateTimeRange=LAST_1h&sort=iops~dsc')




      print("------------------------------------------------------------------")
      print("cluster - storage")
      log.logger('clusters/storage-summary','netapp:storageSummaryList')
      print("------------------------------------------------------------------")
     
      

if __name__ == "__main__":
      main()
      
  
  