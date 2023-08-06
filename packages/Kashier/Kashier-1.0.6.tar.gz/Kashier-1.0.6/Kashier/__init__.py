  
import requests
import hmac
import hashlib
import base64
import json
import urllib
from datetime import datetime
class Invoice(object):
    MID=''
    MODE=''
    CURRENCY=''
    SECRETKEY=''
    totalAmount=0
    URI="https://merchant-id.herokuapp.com"
    URI_TEST="https://merchant-id.herokuapp.com/"
    
    def __init__(self, MID,SECRETKEY, MODE="test",CURRENCY="EGP" ,items=[]):

        self.MID = MID
        self.MODE = MODE 
        self.CURRENCY = CURRENCY
        self.SECRETKEY = SECRETKEY
        self.items=items
  
   
    def init_item(self,description,quantity,unitPrice,itemName,subTotal):
        self.totalAmount+=subTotal
        item=   {
            "description": description,
            "quantity": quantity,
            "itemName": itemName,
            "unitPrice": unitPrice,
            "subTotal": subTotal
            }
        dict_copy = item.copy() # 👈️ 

        self.items.append( dict_copy)
       
        return self.items
    def merchant(self):
        r = requests.get( f'{self.URI }/merchant-data',{}, headers={
            "Content-Type":  "application/json",
             "secret":  self.SECRETKEY,
             "MID":self.MID
        }
            )
        if   not'response' in r.json() : 
             return False
        return r.json()

    
    def create_invoice(self,items, totalAmount,invoiceReferenceId="",tax=0,dueDate=datetime.today().strftime('%Y-%m-%d'),customerName=" ",description=" " ):
     
     
        r = requests.post( f'{self.URI }/invoice', json={
        
        "paymentType": "professional",
        "MID":  self.MID,
        "secret":  self.SECRETKEY,
         "currency": self.CURRENCY,
         "MODE":self.MODE,
        "totalAmount": totalAmount ,
        "customerName": customerName,
        "description": description,
        "dueDate": dueDate,
        "invoiceReferenceId": invoiceReferenceId,
        "invoiceItems":items,
        
        "state": "submitted",
        "tax": tax
        },
        
          headers={"Content-Type":  "application/json"
          ,"MID":self.MID,
          "secret":self.SECRETKEY
          }     
       
            )
        return r.json()
    def share_invoiceBySMS(self,phone ,invoiceReferenceId,storeName="Kashier ",customerName="customer"):
         
        share= {
            "MODE":self.MODE,
            "subDomainUrl": "http://merchant.kashier.io/en/prepay",
            "urlIdentifier": invoiceReferenceId,
            "customerName": customerName,
            "storeName": storeName,
            "secret": self.SECRETKEY,
            "currency": self.CURRENCY,
            "MID": self.MID,
            "customerPhoneNumber": phone,
            "language": "en",
            "operation": "phone"
            }
        r = requests.get( f'{self.URI}/invoice/share', json=share,
         headers={"Content-Type":  "application/json",
          "MID":self.MID,
          "secret":self.SECRETKEY
          }   
            )
        
    
        return r
    def share_invoiceByEmail(self,email ,invoiceReferenceId,storeName=" ",customerName=" "):
          
        share= {
            "MODE":self.MODE,
            "currency": self.CURRENCY,
            "subDomainUrl": "http://merchant.kashier.io/en/prepay",
            "urlIdentifier": invoiceReferenceId,
            "customerName": customerName,
            "storeName": storeName,
            "customerEmail": email,
            "secret": self.SECRETKEY,
            "MID": self.MID,
            "language": "en",
            "operation": "email"
            }
        r = requests.get( f'{self.URI}/invoice/share', json=share,
         headers={"Content-Type":  "application/json",
           "MID":self.MID,
          "secret":self.SECRETKEY
          }   
            )
        return r.json()
        
    
    def get_invoice(self ,invoiceReferenceId): 
        r = requests.get( f"{self.URI}/invoice/{invoiceReferenceId}", json={"MODE":self.MODE,"currency": self.CURRENCY,} ,
         headers={"Content-Type":  "application/json",
                   "MID":self.MID,
                    "secret":self.SECRETKEY
         }  
            )
        return r.json()
    def get_link(self ,invoiceReferenceId): 
        return f'http://merchant.kashier.io/en/prepay/{invoiceReferenceId}?mode={self.MODE}'
    def refund_invoice(self ,invoiceReferenceId,amount):
        
        r = requests.put( f'{self.URI}/invoice/{invoiceReferenceId}', json= {"MODE":self.MODE,"amount":amount} ,
         headers={"Content-Type":  "application/json",
         "MID":self.MID,"secret":self.SECRETKEY}  
            )
        
    
        return r.json()

    def get_list_invoices(self):
       
        r = requests.get( f'{self.URI }/invoice', {"MODE":self.MODE,"currency": self.CURRENCY},
          headers={"Content-Type":  "application/json"
          ,"MID":self.MID,
          "secret":self.SECRETKEY
          }     
            )
        return r.json()
        
    def cancel(self ,invoiceReferenceId):
        r = requests.delete( f'{self.URI}/invoice/{invoiceReferenceId}', json= {"MODE":self.MODE,} ,
         headers={"Content-Type":  "application/json",
         "MID":self.MID,"secret":self.SECRETKEY}  
            )
        
    
        return r.json()

    def set_webhook(self,webhookUrl):

       
        r = requests.post(f'{self.URI }/marchent-webhook',json= {"webhookUrl":webhookUrl ,"MID":self.MID} ,
         headers={"Content-Type":  "application/json",
                                    "MID":self.MID,
                                    "secret":self.SECRETKEY
          }        
            )
    
        return r.json()
    def verify_webhook(self,request, hmac_header=''):
           payload = request.body
           data=json.loads(payload)
           hmac_header = request.headers.get('x-kashier-signature')
           queryString = {}
           for key in data['data']['signatureKeys']:
              queryString[key] = str(data['data'][key])
           secret = bytes(self.SECRETKEY, 'utf-8')
           queryString  = self.http_build_query( queryString).encode()
           
           signature = hmac.new(secret, queryString, hashlib.sha256).hexdigest()
           return signature == hmac_header
    
    def http_build_query(self,data):
      
      
       return urllib.parse.urlencode(data,quote_via=urllib.parse.quote)