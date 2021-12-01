import requests
import sched, time
import pandas as pd
import json
import urllib.parse
import json
from datetime import datetime
from datetime import timedelta
import os
import shutil
import writeOrdersToFile
import ast

url = "https://duroflex.vineretail.com/RestWS/api/eretail/v2/order/status"

headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

dat = input("Enter Start time: format -> DD/MM/YYYY HH:MM:SS (Press enter to assign current date)")
start = ""
end = ""
retrievedOP = ""

def pullOrderDetails(): 
    print("Doing stuff...")

    if dat == "":
      start = datetime.now()
    else:
      start = datetime.strptime(dat, '%d/%m/%Y %H:%M:%S')
      print (start)

    while True:
      print ("Start Date : {}" .format(start))
      end = start + timedelta(hours=1)
      print ("End Date : {}".format(end))

      ''' Date creation '''

      start_date = start.strftime("%d/%m/%Y %H:%M:%S") 
      end_date = end.strftime("%d/%m/%Y %H:%M:%S") 
      
      data = {"order_no":[],"date_from":start_date,"date_to":end_date,"order_location":"","pageNumber":"1"}
      json_str = json.dumps(data,separators=(',', ':'))
      
      #print (json_str)
      str = {'ApiOwner':'Shrijit','ApiKey':'754b261806fe43339313c224ab7603a87b9a5f0d518548de9d3de29','RequestBody':json_str,'OrgId':'DFPL'}

      encoded = urllib.parse.urlencode(str)

      #print (str)

      payload='ApiOwner=Shrijit&ApiKey=754b261806fe43339313c224ab7603a87b9a5f0d518548de9d3de29&RequestBody=%20%7B%0A%20%20%20%22order_no%22%3A%5B%5D%2C%0A%20%20%20%22date_from%22%3A%22{}%2F{}%2F{}%20{}%3A{}%3A{}%22%2C%0A%20%20%20%22date_to%22%3A%22{}%2F{}%2F{}%20{}%3A{}%3A{}%22%2C%0A%20%20%20%22order_location%22%3A%22%22%2C%0A%20%20%20%22pageNumber%22%3A%221%22%0A%20%20%20%20%7D&OrgId=DFPL'.format(start.day,start.month,start.year,start.hour,start.minute,start.second,end.day,end.month,end.year,end.hour,end.minute,end.second)
      #payload=encoded

      response = requests.request("POST", url, headers=headers, data=payload)

      retrievedOP = response.text
      #print(response.text)
      '''with open("sample.json","r+") as file1:
        file1.write(response.text)
        file1.close()'''
      createOrderRecrd(retrievedOP)
           
      time.sleep(1800)

      if start+timedelta(hours=1) == datetime.now():
        start = end

def createOrderRecrd(str):
    dir = 'vinorderin'
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

    # Opening JSON file
    #f = open('sample.json',)

    #data = json.load(f)

    data = json.loads(str)
    #print (data)

    if data['order'] == None:
        print ("No Records found for the given time period")
    else:
        print ("Records found for the given time period")
        print ("Records written to vinorderin")
        for i in data['order']:
            delimiter = " | "
            headers = ['order_no','eretailOrderNo','masterOrderNo','status','grandtotal','createAtStoreDate','shippingaddress','mobileno','sku','order_qty','internalLineNo','price','weight']
            values = []
            


            with open("vinorderin/{}.txt".format(i['order_no']), "w") as f:
                f.write("|".join(headers))
                f.write("\n")
                for j in i['shipdetail']:
                    for z in j['item']:
                        values = [i['order_no'] , i['eretailOrderNo'], i['masterOrderNo'], i['status'], i['grandtotal'], i['createAtStoreDate'], i['shippingaddress'], i['mobileno']]
                        values.append(z['sku'])
                        values.append(z['order_qty'])
                        values.append(z['internalLineNo'])
                        values.append(z['price'])
                        values.append(j['weight'])
                        f.write("|".join(values))
                        f.write("\n")
                
                f.close()
      

            
pullOrderDetails()




