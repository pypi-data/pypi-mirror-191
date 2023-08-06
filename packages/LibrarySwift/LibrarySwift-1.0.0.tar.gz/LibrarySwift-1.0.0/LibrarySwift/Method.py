from SwiftRubika.Configs import welcome , web , android , encryptio
from SwiftRubika.SendData import http,httpfiles
from SwiftRubika.GetAdress import server_bot
import datetime
from json import dumps, loads
from datetime import datetime
import asyncio
import datetime
from asyncio import run
from re import findall
from random import randint, choice
from os import system
from requests import post, get
from colorama import Fore as color
	
class send_server_rubika:
    
    def server_full(self):
        return choice(server_bot.list_servers)

    def server_files(self):
        return choice(server_bot.list_servers)
        
class Client:
    ser_full = send_server_rubika()
    server_rubi = ser_full.server_full()
    
    def __init__(self, auth_account: str):
        self.auth = str("".join(findall(r"\w",auth_account)))
        self.enc = encryptio(auth_account)
        self.print = welcome
        
        if self.auth.__len__() < 32:
        	print(color.RED+"Error : Your auth is invalid, Please check and try again ."),exit()
        else:
            if self.auth.__len__() > 32:
            	print(color.RED+"Error : Your auth is invalid, Please check and try again ."),exit()

    def requests_method(self, method):
        while 1:
            try:
                loop = asyncio.get_event_loop()
                requests = self.enc.decrypt(loads(loop.run_until_complete(http(Client.server_rubi,self.auth,method))).get("data_enc"))
                return loads(requests)
                break
            except: continue
      
#message

    def send_message(self, chat_id,text,metadata=[],message_id=None):
        method = {"method":"sendMessage",
        "input":{
                "object_guid":chat_id,
                "rnd":f"{randint(100000,999999999)}",
                "text":text,
                "reply_to_message_id":message_id
            },
            "client": web
        }
        if metadata != [] : method["input"]["metadata"] = {"meta_data_parts":metadata}
        return self.requests_method(method)
        
    def edit_message(self, gap_guid, new_text, message_id):
        method = {"method":"editMessage",
        "input":{
                "message_id":message_id,
                "object_guid":gap_guid,
                "text":new_text
            },
            "client": web
        }
        return self.requests_method(method)
        
    def delete_messages(self, chat_id, message_id):
        method = {"method":"deleteMessages",
        "input":{
                "object_guid":chat_id,
                "message_ids":message_id,
                "type":"Global"
            },
            "client": web
        }
        return self.requests_method(method)
        
    def forward_messages(self, From, message_ids, to):
        method = {"method":"forwardMessages",
			"input":{
				"from_object_guid": From,
				"message_ids": message_ids,
				"rnd": f"{randint(100000,999999999)}",
				"to_object_guid": to
            },
            "client": web
        }
        return self.requests_method(method)
        
    def get_messages(self, chat_id, min_id):
        method = {"method":"getMessagesInterval", 
        "input":{
                "object_guid":chat_id,
                "middle_message_id":min_id
            },
            "client": web
        }
        return self.requests_method(method).get("data").get("messages")
        
    def get_chats(self, start_id=None):
        method = {"method":"getChats",
        "input":{
                "start_id":start_id
            },
            "client": web
        }
        return self.requests_method(method).get("data").get("chats")

    def get_messages_Info(self, chat_id, message_ids):
        method = {"method":"getMessagesByID",
        "input":{
                "object_guid": chat_id,
                "message_ids": message_ids
            },
            "client": android
        }
        return self.requests_method(method).get("data").get("messages")
        
    def delete_user_chat(self, user_guid, last_message):
        method = {"method":"deleteUserChat",
        "input":{
                "last_deleted_message_id":last_message,
                "user_guid":user_guid
            },
            "client": web
        }
        return self.requests_method(method)
        
    def get_info_by_username(self, username):
        method = {"method":"getObjectByUsername",
        "input":{
                "username":username
            },
            "client": web
        }
        return self.requests_method(method)
        
    def ban_group_member(self, chat_id, user_id):
        method = {"method":"banGroupMember",
        "input":{
                "group_guid": chat_id,
                "member_guid": user_id,
                "action":"Set"
            },
            "client": web
        }
        return self.requests_method(method)
        
    def unban_group_Member(self, chat_id, user_id):
        method = {"method":"banGroupMember",
        "input":{
                "group_guid": chat_id,
                "member_guid": user_id,
                "action":"Unset"
            },
            "client": android
        }
        return self.requests_method(method)
        
    def get_group_info(self, group_guid):
        method = {"method":"getGroupInfo",
        "input":{
                "group_guid": group_guid
            },
            "client": web
        }
        return self.requests_method(method) 
        
    def get_channel_info(self, channel_guid):
        method = {"method":"getChannelInfo",
        "input":{
                "channel_guid":channel_guid
            },
            "client": android
        }
        return self.requests_method(method)
        
    def add_group_members(self, chat_id, user_ids):
        method = {"method":"addGroupMembers",
        "input":{
                "group_guid": chat_id,
                "member_guids": user_ids
            },
            "client": web
        }
        return self.requests_method(method)
        
    def add_channel_Members(self, chat_id, user_ids):
        method = {
            "method":"addChannelMembers",
            "input":{
                "channel_guid": chat_id,
                "member_guids": user_ids
            },
            "client": web
        }
        return self.requests_method(method)
        
    def get_group_admins(self, chat_id):
        method = {"method":"getGroupAdminMembers",
        "input":{
                "group_guid":chat_id
            },
            "client": android
        }
        return self.requests_method(method)

    def get_group_members(self, chat_id, start_id=None):
        method = {"method":"getGroupAllMembers",
        "input":{
                "group_guid": chat_id,
                "start_id": start_id
            },
            "client": web
        }
        return self.requests_method(method)
        
    def set_members_access(self, chat_id, access_list):
        method ={"method":"setGroupDefaultAccess",
            "input":{
                "access_list": access_list,
                "group_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method)
        
    def get_link_from_url(self, app_url):
        method = {"method":"getLinkFromAppUrl",
            "input":{
                "app_url":app_url
            },
            "client": android
        }
        return self.requests_method(method).get("data").get("link").get("open_chat_data")
        
    def join_channel_by_link(self, link):
        hashLink = link.split("/")[-1]
        method = {"method":"joinChannelByLink",
            "input":{
                "hash_link":hashLink
            },
            "client": android
        }
        return self.requests_method(method)
        
    def join_channel_by_id(self, chat_id:str):
        id = chat_id.split("@")[-1]
        guid = Client.get_info_by_username(self,id)["data"]["channel"]["channel_guid"]
        method = {"method":"joinChannelAction",
            "input":{
                "action": "Join",
                "channel_guid": guid
            },
            "client": android
        }
        return self.requests_method(method)
        
    def join_channel_by_guid(self, chat_id:str):
        method = {"method":"joinChannelAction",
            "input":{
                "action": "Join",
                "channel_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method)
        
    def join_group(self, link):
        hashLink = link.split("/")[-1]
        method = {"method":"joinGroup",
            "input":{
                "hash_link": hashLink
            },
            "client": android
        }
        return self.requests_method(method)
        
    def leave_group(self,chat_id):
        method = {"method":"leaveGroup",
            "input":{
                "group_guid": chat_id
            },
            "client": android
        }
        return self.requests_method(method)