import requests

url = "https://192.168.1.35/rest/events?limit=20"

payload  = {}
headers = {
  'Accept': ' application/vnd.netapp.object.inventory.hal+json',
  'Authorization': 'Basic YWRtaW46UEBzc3cwcmQxMjM='
}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))