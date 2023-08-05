
import os
import requests
import sys
import json
from enum import Enum
from airbyte_cdk.models import AirbyteConnectionStatus,Status

class IPFSSource:
    """
    Source connector for IPFS Source .
    This function is used to initialize a IPFSSource object and is called when creating an instance of this class.
    It takes in a configuration dictionary containing the relevant IPFS link information necessary .

        Configuration parameters in json format:
        - IPFSURL (string): link to fetch data from ipfs source.
              
    """

    def __init__(self, config: dict, clientSelf):
        self.IPFSURL = config["IPFSURL"]
        self.APIBaseURL = config["APIBaseURL"]
        self.clientSelf = clientSelf
       

    def getToken(self,email,password):
        try:
            params = {'email':email,'password':password}
            api= str(self.APIBaseURL) + "getToken"
            # print(url)
            resp = requests.get(api,params=params,verify=False) 
            if resp.status_code != 200:
                return "authentication failed"
            else :
                return resp.text

        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to authenticate: {str(e)}")


    def check(self,token)-> AirbyteConnectionStatus:
        """
        This check() function is used to check if the url  connection is successful.
        It attempts to connect to the IPFS url provided by user  and prints a success message if successful.
        """
        try:
            headers={'Authorization':f"Bearer {token}"} 
            api= str(self.APIBaseURL) +"validateUser"
            resp = requests.get(api,headers=headers,verify=False) 
            if resp.status_code != 200:
                return "authentication failed"

            f = requests.get(self.IPFSURL)
            if f.ok :
                self.clientSelf.logInfo(self.clientSelf.step, 'IPFS  connection successful')
                return AirbyteConnectionStatus(status=Status.SUCCEEDED)
            else :
                self.clientSelf.logError(self.clientSelf.step, f"Failed to load IPFS url provided: {str(f._content)}")
                return AirbyteConnectionStatus(status=Status.FAILED,message=str(f._content))
            
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to load IPFS url provided: {str(e)}")


    

    def read(self,token):
        """
        Read content and store it at temperory location.
        
        """

        try:

            headers={'Authorization':f"Bearer {token}"} 
            api= str(self.APIBaseURL) + "validateUser"
            resp = requests.get(api,headers=headers,verify=False) 
            if resp.status_code != 200:
                return "authentication failed"

            streamData = requests.get(self.IPFSURL)
            if streamData.ok :
                self.clientSelf.logInfo(self.clientSelf.step, ' Read Data successful')
                return  streamData
            else :
                self.clientSelf.logError(self.clientSelf.step, f"Failed to load IPFS url provided: {str(streamData._content)}")
                return streamData
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to fetch the data: {str(e)}")


        
        