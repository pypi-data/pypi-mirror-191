import func_timeout
import requests
import json
from enum import Enum
import logging
import socket
import re
import math
import asyncio


class Venta_Protocol_v3_Device:
    """Class representing a Venta Device that uses Protocol V3

    Attributes:
        Automatic (int): 1 if device is in Automatic mode, 0 if it's not
        BaLi (int): ???
        DaysToService (int): Number of days until device needs to be serviced (not provided by device directly but calulated from ServiceT and ServiceMax)
        DeviceType (str): Type of the device
        FanSpeed (int): Current Fan Speed setting (1,2,3)
        Humidity (float): Current Humidity reading
        HwIndexMB (str): ???
        IP (str): IP Address of the device
        MacAdress (str): Max Address of the device (wrong spelling is part of the protocol, so not fixing the property name to avoid confusion)
        OperationT (int): Total device uptime
        Power (int): 1 if device is powered on, 0 if it's not
        ProtocolV (str): Version of the communication protocol used (this library only supports v3.0)
        SWMain (str): Firmware version
        ServiceMax (int): Service interval
        ServiceT (int): Time in operation since last service
        SleepMode (int): 1 if Sleep Mode is active, 0 if it's not
        TargetHum (int): Target humidity that the device tries to reach. Only has an effect when Automatic Mode is enabled. The original app only allows values to be set in 5% steps (40,45,50,..), so any other values may be unsupported.
        Temperature (int): Current Temperature reading
        Warnings (int): ???
    """
    
    @staticmethod
    async def discoverDevices(durationSeconds:int = 10):
        """Static method to run discovery of Venta V3 Decices on the network. The duration this method listens for broadcasts can be adjusted with the durationSeconds parameter
        
        Args:
            durationSeconds (int): How long to run the discovery in seconds

        Returns:
            list: A list of discovered devices
        """
        Devices=[]
        def disco():
            UDP_IP = "255.255.255.255"
            UDP_PORT = 48000

            sock = socket.socket(socket.AF_INET, # Internet
                                 socket.SOCK_DGRAM) # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            sock.bind((UDP_IP, UDP_PORT))

            while True:
                data, addr = sock.recvfrom(1024)
                js = re.findall("{.+}", str(data))
                if len(js) > 0:
                    obj = json.loads(js[0])
                    if obj["Header"]["ProtocolV"]=="3.0":
                        if len([x for x in Devices if x["MacAdress"] == obj["Header"]["MacAdress"]])==0:
                            Devices.append(obj["Header"])

        
        try:
            return func_timeout.func_timeout(durationSeconds, disco)
        except func_timeout.FunctionTimedOut:
            pass
        return Devices    
        
    def __init__(self, IP:str):
        """Constructor takes the IP Address of the device as parameter
                
        Args:
            IP (str): The IP Address of the Venta device

        Returns:
            None
        """
        self.IP:str = IP
        self.Automatic:int=0
        self.BaLi:int=0
        self.DaysToService:int=0
        self.DeviceType:str=""
        self.FanSpeed:int=0
        self.Humidity:float=0
        self.HwIndexMB:str=""
        self.MacAdress:str=""
        self.OperationT:int=0
        self.Power:int=0
        self.ProtocolV:str=""
        self.SWMain:str=""
        self.ServiceMax:int=0
        self.ServiceT:int=0
        self.SleepMode:int=0
        self.TargetHum:int=0
        self.Temperature:int=0
        self.Warnings:int=0
        
    def getStatus(self):
        """Contacts the Venta device and populates / updates the class properties""" 
        self._makeCall("/api/telemetry")

    def setAutomatic(self, target:bool):
        """Enables / disables the Automatic mode of the Venta device
        
        Args:
            target (bool): The target state for Auto Mode
            
        Returns:
            bool: Success of the operation
        """
        self._makeCall("/api/telemetry?request=set", {"Power":1, "Automatic": int(target), "Action":"control"})
        return self.Automatic == int(target);
    
    def setSleepMode(self, target:bool):
        """Enables / disables the Sleep mode of the Venta device    
        
        Args:
            target (bool): The target state for Sleep Mode
            
        Returns:
            bool: Success of the operation
        """
        self._makeCall("/api/telemetry?request=set", {"SleepMode": int(target), "Action":"control"})
        return self.SleepMode == int(target);
        
    def setFanSpeed(self, target:int):
        """Sets the Fan Speed of the Venta device    
        
        Args:
            target (int): The target fan speed [1,2,3]
            
        Returns:
            bool: Success of the operation
        """
        self._makeCall("/api/telemetry?request=set", {"Power":1, "FanSpeed": int(target), "Automatic":0, "Action":"control"})
        return self.FanSpeed == int(target);
    
    def setTargetHum(self, target:int):
        """Sets the target humidity of the Venta device    
        
        Args:
            target (int): The target humidity (in 5% steps)
            
        Returns:
            bool: Success of the operation
        """
        self._makeCall("/api/telemetry?request=set", {"TargetHum":int(target), "Action":"control"})
        return self.TargetHum == int(target);
    
    def setPower(self, target:bool):
        """Enables / disables the the Venta device    
        
        Args:
            target (bool): The target state for Power
            
        Returns:
            bool: Success of the operation
        """
        self._makeCall("/api/telemetry?request=set", {"Power":int(target), "FanSpeed":1, "SleepMode":0, "Automatic":0, "Action":"control"})
        return self.Power == int(target);

    def _makeCall(self, endpoint:str, payload:dict=None):
        """Handle API calls and trigger update of class properties    
        
        Args:
            endpoint (str): The endpoint to invoke (Currently known to exist: "/api/telemetry" or "/api/telemetry?request=set")
            payload (str, optional): The payload to send to the endpoint
            
        Returns:
            dict: Response body
        """
        logging.debug("Sending payload to endpoint " + "http://"+self.IP+endpoint + ":\n" + str(payload)+"\n")
        r  = requests.post("http://"+self.IP+endpoint, json=payload)
        obj = json.loads(r.text)
        self._processResponse(obj)
        return obj
        
    def _processResponse(self, response:dict):
        """Process responses from the Venta device    
        
        Args:
            response (dict): The response body from the venta device
            
        Returns:
            None
        """
        logging.debug("Processing response:\n" + str(response)+"\n")
        self._walkProperties(response, callback=lambda prop, value: setattr(self,prop,value))
        setattr(self,"DaysToService",math.ceil((self.ServiceMax-self.ServiceT)/144))
        
    def _walkProperties(self, obj:dict, callback:callable, maxDepth:int=3):
        """Walks through all properties of a dict recursively and calls the "callback" function for each property. Max recursion depth is configurable.    
        
        Args:
            obj (dict): The object to walk through
            callback (callable): The function to be called for each property
            maxDepth (int, optional): The max recursion depth (default=3)
        
        Raises:
            ValueError: If max recursion depth is reached.
            
        Returns:
            None
        """
        if maxDepth > 0:
            for prop in obj:
                if isinstance(obj[prop],dict):
                    self._walkProperties(obj[prop], callback, maxDepth=maxDepth-1)
                else:
                    callback(prop, obj[prop])
        else:
            raise ValueError("Error processing response - max recursion depth reached. This could happen if the device sent an unexpected response. Check preceding log entries to verify response object.")
    
    def toJSON(self):
        """Return JSON of all properties"""
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)