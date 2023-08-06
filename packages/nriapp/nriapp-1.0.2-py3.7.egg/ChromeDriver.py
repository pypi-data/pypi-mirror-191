#!/usr/bin/python
import os, sys
import time
import requests, json, pickle, ast
import queue
import re
from core import msgraphapi as graphapi 
from core import mssentinelapi as defender
from core import multifactor as mfaauth
from core.abuseipdbapi import ipquery
from helper import requestheader as helper
from helper import login
from helper.doc import *
from helper.doc import WordDoc
from loguru import logger
from docx import Document
import argparse
from datetime import datetime
from dateutil import parser
import pytz    
import json
from config.config import *
import configparser

requests.packages.urllib3.disable_warnings()        #Disable requests warning logs

logger.add(f"./logs/{__name__}.log", mode="w", backtrace=True, diagnose=True, level="ERROR", filter="ChromeDriver")
#logger.disable(__name__)
dbgPrint = logger

tz = pytz.timezone('Asia/Hong_Kong')

class NriApp:
    def __init__(self, args):
        self.args = args
#        self.email = self.args.get("email", "")
#        self.output = self.args.get("output",  os.path.abspath(os.path.dirname(__file__)) + "\\output")
        self.config = configparser.ConfigParser()

        if args.get("email"):
            self.write_config()
        else:
            self.read_config()


        if self.email and not hasattr(self, "msgraph"):
            self.msgraph = graphapi.MSGraphApi(self.email).load_session()
            self.mfa = mfaauth.MultiFactor(self.email).load_session()
            self.sentinel = defender.MSSentinelApi(self.email).load_session()
        else:
            dbgPrint.error("Email does not exist")
            dbgPrint.info("Would you like to setup first? Use -h")

    def write_config(self):
        if self.args.get("email"):
            self.config.add_section('email')
            self.config['email']['address'] = self.args["email"]
            self.email = self.args["email"]
            if self.args.get("output"):
                self.config.add_section('folder')
                self.config['folder']['output'] = self.args["output"]
                self.output = self.args["output"]

            else:
                self.config.add_section('folder')
                self.config['folder']['output'] = os.path.abspath(os.path.dirname(__file__))
                self.output = os.path.abspath(os.path.dirname(__file__)) + "\\output"


            if not os.path.exists(self.output):
                os.makedirs(self.output)
            with open(os.path.abspath(os.path.dirname(__file__)) + '\config.ini', 'w') as configfile:
                self.config.write(configfile)

            dbgPrint.info("Config has been setup.")
            return True
        else:
            return False
            

    def read_config(self):

        if os.path.exists(os.path.abspath(os.path.dirname(__file__)) + '\\config.ini'):
            self.config.read(os.path.abspath(os.path.dirname(__file__)) + '\\config.ini')
            if self.config.has_section('email'):
                self.email = self.config['email']['address']   
            else:
                dbgPrint.error("No email found in config.ini. Use -e or --email=<email address>")
                sys.exit()
            if self.config.has_section('folder'):
                self.output = self.config['folder']['output']
        else:
            dbgPrint.error("No config.ini yet. Use -e/--email")
            sys.exit()


    def user_summary(self, query):
        user_object = self.msgraph.search_user(query)[0] if self.msgraph.search_user(query) else {}
        temp = {}
        if user_object:
            if user_object["companyName"] != None:
                temp["companyName"] = user_object["companyName"]
            if user_object["country"] != None:
                temp["country"] = user_object["country"]
            if user_object["displayName"] != None:
                temp["name"] = user_object["displayName"]
            if user_object["userPrincipalName"] != None:
                temp["email"] = user_object["userPrincipalName"]
                mfa = self.msgraph.check_mfa_status(user_object["userPrincipalName"])
                if mfa:
                    temp["MFAStatus"] = mfa[0]["isMfaRegistered"]
                else:
                        temp["MFAStatus"] = "Probably not registered"
            if query != None:
                temp["groups"] = self.msgraph.get_user_groups(query)
        return temp

        def ip_summary(self, param, ip_list):
            ip = param.get("senderIP", "")
            if ip:
                return list(set(ip + ip_list))
            else:
                return ip_list

    def file_summary(self, param, hash_list):
        def walk_dict(object, list_object):
            if isinstance(object, dict):
                for k,v in object.items():
                    if isinstance(v, dict):
                        walk_dict(v, list_object)
                    elif isinstance(v, list):
                        for a in v:
                             walk_dict(a, list_object)
                    elif isinstance(v, str) or isinstance(v, int):
                        if k == "hash" or k == "sha256" or k == "sha1":
                            if v.lower() not in list_object:
                                list_object.append(v)
            elif isinstance(object, list):
                for a in object:
                    walk_dict(a, list_object)
            return list_object
      
        hash_list = walk_dict(param, hash_list)
        return hash_list

    def recipient_summary(self, param, hash_list):
        def walk_dict(object, list_object):
            if isinstance(object, dict):
                for k,v in object.items():
                    if isinstance(v, dict):
                        walk_dict(v, list_object)
                    elif isinstance(v, list):
                        for a in v:
                             walk_dict(a, list_object)
                    elif isinstance(v, str) or isinstance(v, int):
                        if k == "recipient":
                            if v.lower() not in list_object:
                                list_object.append(v)
            elif isinstance(object, list):
                for a in object:
                    walk_dict(a, list_object)
            return list_object
      
        hash_list = walk_dict(param, hash_list)
        return hash_list

    def summary(self, param):
        data = {}
        incidentId = param["IncidentId"]
        title = param["Title"]
        categories = param["Categories"]
        severity = [k for k,v in param["AlertsSeveritiesSummary"].items()]
        computerName = param["ComputerDnsName"]
        firstActivity = param["FirstEventTime"]
        lastActivity = param["LastEventTime"]
        deviceTags = param["IncidentTags"]["DeviceTags"]
        machines = param["ImpactedEntities"]["Machines"]
        users = param["ImpactedEntities"]["Users"]
        mailboxes = param["ImpactedEntities"]["Mailboxes"]
        dSource = param["DetectionSources"]

        source = []
        for i in dSource:
            if i == 512:
                source.append("Microsoft Defender for Office 365 (MDO)")
            elif i == 2:
                source.append("Antivirus")
            elif i == 1:
                source.append("Endpoint Detection and Response (EDR)")
            elif i == 4:
                source.append("SmartScreen")
            elif i == 65536:
                source.append("Identity Protection")
            elif i == 16384:
                source.append("Microsoft Defender for Cloud Apps (MCAS)")
            elif i == 32768:
                source.append("Microsoft 365 Defender")
            else:

                dbgPrint.error("Unknown source %s", i)
                pass

        users_list = []
        for i in users:
            temp = {}
            displayName = i["DisplayName"]
            userName = i["UserName"]
            userSid = i["UserSid"]
            query = ""
            if displayName != None:
                query = displayName
            elif userName != None:
                query = userName
            elif userSid != None:
                query = userSid
            user_object = self.msgraph.search_user(query)[0] if self.msgraph.search_user(query) else {}
            if user_object:
                if user_object["companyName"] != None:
                    temp["companyName"] = user_object["companyName"]
                if user_object["country"] != None:
                    temp["country"] = user_object["country"]
                if user_object["displayName"] != None:
                    temp["name"] = user_object["displayName"]
                if user_object["userPrincipalName"] != None:
                    temp["email"] = user_object["userPrincipalName"]
                    mfa = self.msgraph.check_mfa_status(user_object["userPrincipalName"])
                    if mfa:
                        temp["MFAStatus"] = mfa[0]["isMfaRegistered"]
                    else:
                         temp["MFAStatus"] = "Probably not registered"
                if query != None:
                    temp["groups"] = self.msgraph.get_user_groups(query)
            
                users_list.append(temp)

        device_list = []
        for i in machines:
            temp = {}
            computerName = i["ComputerDnsName"]
            exposureScore = i["ExposureScore"]
            device_object = self.msgraph.search_device_by_name(computerName.split(".")[0])[0] if self.msgraph.search_device_by_name(computerName.split(".")[0]) else {}
            if device_object:
                if device_object["deviceName"] != 'none':
                    temp["deviceName"] = device_object["deviceName"]
                if device_object["complianceState"] != 'none':
                    temp["complianceState"] = device_object["complianceState"]
                if device_object["osVersion"] != 'none':
                    temp["osVersion"] = device_object["osVersion"]
                if device_object["userPrincipalName"] != 'none':
                    user_object = self.msgraph.search_user(device_object["userPrincipalName"])[0] if self.msgraph.search_user(device_object["userPrincipalName"]) else {}
                    user = {}
                    temp["userPrincipalName"] = user
                    if user_object:
                        if user_object["companyName"] != None:
                            user["companyName"] = user_object["companyName"]
                        if user_object["country"] != None:
                            user["country"] = user_object["country"]
                        if user_object["userPrincipalName"] != None:
                            user["email"] = user_object["userPrincipalName"]
                            user["MFAStatus"] = self.msgraph.check_mfa_status(user_object["userPrincipalName"])[0]["isMfaRegistered"] if self.msgraph.check_mfa_status(user_object["userPrincipalName"]) else {}
                        if user_object["displayName"] != None:
                            user["name"] = user_object["displayName"]
    #                temp["userPrincipalName"] = device_object["userPrincipalName"]
                    user["groups"] = self.msgraph.get_user_groups(device_object["userPrincipalName"])
                device_list.append(temp)

        mailbox_list = []
        for i in mailboxes:
            temp = {}
            userPrincipalName = i["Upn"]
            user_object = self.msgraph.search_user(userPrincipalName)[0] if self.msgraph.search_user(userPrincipalName) else {}
            if user_object:
                if user_object["companyName"] != None:
                    temp["companyName"] = user_object["companyName"]
                if user_object["country"] != None:
                    temp["country"] = user_object["country"]
                if user_object["userPrincipalName"] != None:
                    temp["email"] = user_object["userPrincipalName"]
                if user_object["displayName"] != None:
                    temp["name"] = user_object["displayName"]
                temp["groups"] = self.msgraph.get_user_groups(userPrincipalName)
                mailbox_list.append(temp)
        
        impactedAssets = {"users"       : users_list, 
                         "machines"     : device_list,
                         "mailboxes"    : mailbox_list
                         }


        data["incidentId"]      = incidentId
        data["title"]           = title
        data["categories"]      = categories
        data["severity"]        = severity
        if computerName:
            data["computerName"]    = computerName
        if source:
            data["detectionSource"] = source
        utc_time = parser.parse(firstActivity)
        utc_time = utc_time.replace(tzinfo=pytz.UTC) #replace method      
        ph_time=utc_time.astimezone(tz)        #astimezone method
        data["firstActivity"]   = ph_time.strftime('%Y-%m-%d %H:%M:%S GMT+8')
        utc_time = parser.parse(lastActivity)
        utc_time =utc_time.replace(tzinfo=pytz.UTC) #replace method      
        ph_time=utc_time.astimezone(tz)        #astimezone method
        data["lastActivity"]    = ph_time.strftime('%Y-%m-%d %H:%M:%S GMT+8')
        data["deviceTags"]      = deviceTags
        data["impactedAssets"]  = impactedAssets

        return data
    
    def ip_summary(self, param, ip_list):
        ip = param.get("senderIP", "")
        if ip:
            return list(set(ip + ip_list))
        else:
            return ip_list


    def get_full_report(self, args=None, lookBackInDays=180):
        incidents = self.sentinel.get_incidents(incidentId=args, alertStatus=['New','InProgress', 'Resolved'] , severity=[256,128,64,32], pageIndex=1, lookBackInDays=lookBackInDays, pageSize=3000, sourceFilter=[16384, 65536, 1048576])       #16384 == MCAS incidents 512 = eDiscovery
        if args != None:
            all_data = {}
#            incidents = self.sentinel.get_incidents(incidentId=args, alertStatus=['New','InProgress', 'Resolved'] , severity=[256,128,64,32], pageIndex=1, lookBackInDays=180, pageSize=3000, sourceFilter=[16384, 65536, 1048576])       #16384 == MCAS incidents 512 = eDiscovery
            docu2 = new_doc()
            doc = WordDoc()
            ip_list = []
            hash_list = []
            recipient = []
            for i in range(1):
                q = queue.Queue()    
                self.sentinel.get_associated_evidences(args, queue=q, lookBackInDays = lookBackInDays)
                out = self.summary(incidents[0])
                doc.title(out["title"])
                doc.author(self.email)
                doc.traverse(out)
                all_data = self.sentinel.accumulate(q)
                for a in all_data:
                    doc.insertHR(doc.insert_paragraph())

                    doc.traverse(a)

                    ip_list = self.ip_summary(a, ip_list)
                    hash_list = self.file_summary(a, hash_list)
                    recipient = self.recipient_summary(a, recipient)

            doc.insertHR(doc.insert_paragraph())
            doc.add_run("Additional Details")
            doc.traverse([ipquery.check_endpoint(i) for i in ip_list])
            doc.insertHR(doc.insert_paragraph())
            doc.traverse([self.sentinel.get_file_info(i) for i in hash_list])
            doc.insertHR(doc.insert_paragraph())
            doc.traverse([self.user_summary(i) for i in recipient])
            doc.insertHR(doc.insert_paragraph())
            doc.traverse(self.sentinel.get_audit_history(args))
            doc.save(self.output + "\\" + args + ".docx")
            os.startfile(self.output + "\\" + args + ".docx")

        else:
            all_data = {}
            for count, i in enumerate(incidents, start=1):
                doc = WordDoc()
                ip_list = []
                hash_list = []
                recipient = []
                q = queue.Queue()
                out = self.summary(i)
                doc.title(out["title"])
                doc.author(self.email)
                doc.traverse(out)
                self.sentinel.get_associated_evidences(i["IncidentId"], queue=q, lookBackInDays=lookBackInDays)   
                dbgPrint.info(i["IncidentId"])
                all_data = self.sentinel.accumulate(q)
                for a in all_data:
                    doc.insertHR(doc.insert_paragraph())
                    ip_list = self.ip_summary(a, ip_list)
                    hash_list = self.file_summary(a, hash_list)
                    recipient = self.recipient_summary(a, recipient)

                    doc.traverse(a)

                doc.insertHR(doc.insert_paragraph())
                doc.add_run("Additional Details")
                doc.traverse([ipquery.check_endpoint(i) for i in ip_list])
                doc.insertHR(doc.insert_paragraph())
                doc.traverse([self.sentinel.get_file_info(i) for i in hash_list])
                doc.insertHR(doc.insert_paragraph())
                doc.traverse([self.user_summary(i) for i in recipient])
                doc.insertHR(doc.insert_paragraph())
                doc.traverse(self.sentinel.get_audit_history(i["IncidentId"]))
                doc.save(self.output + "\\" + str(i["IncidentId"]) + ".docx")
#                os.startfile(self.output + "\\output\\" + str(i["IncidentId"]) + ".docx")    

    def dispatcher(self):
        args = self.args
        dbgPrint.disable(__name__)
        path = os.path.dirname(os.path.realpath(__file__))
        if args.get("verbose") == True:
            dbgPrint.enable(__name__)
        if args.get("clear"):
            pass
        if args.get("user"):
            self.__init__(args)
            user_info = self.msgraph.check_mfa_status(args.get("user"))
#            if user_info:
#                printTable(user_info)
#            user_info = self.msgraph.search_user(args.get("user"))
        elif args.get("incidentId"):
            self.__init__(args)
            self.get_full_report(args.get("incidentId"), lookBackInDays=args.get("daysgo", 180))
        else:
            self.get_full_report(lookBackInDays=args.get("daysgo", 180))
            return

    #------------------------------------------------------

def parse_argument():

    parser = argparse.ArgumentParser(
        prog = 'ChromeDriver',
        description  = 'This tool is used to retrieve all the necessary informaation of the incident',
        epilog = ''
        )

    parser.add_argument('-id', '--incidentId',help="Id number")
    parser.add_argument('-v', '--verbose', help="Disable logging" , action="store_true")
    parser.add_argument('-r', '--reset', help="Reset the session and restart", action="store_true")
    parser.add_argument('-e', '--email', help="Email address")
    parser.add_argument('-u', '--user', help = "Fetch user info")
    parser.add_argument('-o', '--output', help = "Output folder")
    parser.add_argument('-c','--clear', help = "Clear cache", action="store_true")
    parser.add_argument('-d', '--daysago', help="Look back in days. Default=180")


    args = parser.parse_args()

    return args 

if __name__ == "__main__":

    args = parse_argument()
    myapp = NriApp(vars(args))
    myapp.dispatcher()
#    main(args)