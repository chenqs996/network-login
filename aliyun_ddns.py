from __future__ import print_function
import json
import os,sys
import re
from datetime import datetime
import socket

from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordInfoRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest

# 返回内容格式

            
class aliyun_ddns:
    rc_format = 'json'
    access_key_id = str()
    access_key_secret = str()
    dns_domain = str()
    rc_rr_list = list()

    def __init__(self, access_key_id, access_key_secret, dns_domain, rc_rr_list):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.dns_domain = dns_domain
        self.rc_rr_list = rc_rr_list
    """
    获取域名的解析信息
    """
    def check_records(self):
        clt = client.AcsClient(self.access_key_id, self.access_key_secret)
        request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        request.set_DomainName(self.dns_domain)
        request.set_accept_format(self.rc_format)
        result = clt.do_action(request).decode('utf-8')
        result = json.JSONDecoder().decode(result)
        return result

    """
    根据域名解析记录ID查询上一次的IP记录
    """
    def get_old_ip(self, record_id):
        clt = client.AcsClient(self.access_key_id,self.access_key_secret,'cn-hangzhou')
        request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
        request.set_RecordId(record_id)
        request.set_accept_format(self.rc_format)
        result = clt.do_action(request)
        result = json.JSONDecoder().decode(result.decode('utf-8'))
        result = result['Value']
        return result

    """
    更新阿里云域名解析记录信息
    """
    def update_dns(self, dns_rr, dns_type, dns_value, dns_record_id, dns_ttl):
        clt = client.AcsClient(self.access_key_id, self.access_key_secret, 'cn-hangzhou')
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_RR(dns_rr)
        request.set_Type(dns_type)
        request.set_Value(dns_value)
        request.set_RecordId(dns_record_id)
        request.set_TTL(dns_ttl)
        request.set_accept_format(self.rc_format)
        result = clt.do_action(request)
        return result

    def write_to_file(self, new_ip ,rc_rr):
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        write_log = open('aliyun_ddns.txt', 'a')
        write_log.write(('%s %s %s.%s\n')%(time_now,str(new_ip),rc_rr,self.dns_domain))
        return

    def ddns(self, now_ip):
        dns_records = self.check_records()
        for rc_rr in self.rc_rr_list:
            ## 之前的解析记录
            old_ip = ""
            record_id = ""
            for record in dns_records["DomainRecords"]["Record"]:
                if record["Type"] == 'A' and record["RR"] == rc_rr:
                    record_id = record["RecordId"]
                    print("%s.%s recordID is %s" % (record["RR"],self.dns_domain,record_id))
                    if record_id != "":
                        old_ip = self.get_old_ip(record_id)
                        break
            
            if record_id  == "":
                print(('Warning: Can not find record_id with A record: %s in %s. Please add it first!')%(rc_rr,self.dns_domain))
                continue

            print("%s.%s now host ip is %s, dns ip is %s" % (rc_rr, self.dns_domain, now_ip, old_ip))

            if old_ip == now_ip:
                print("The specified value of parameter Value is the same as old")
            else:
                rc_type = 'a'               # 记录类型, DDNS填写A记录
                rc_value = now_ip           # 新的解析记录值
                rc_record_id = record_id    # 记录ID
                rc_ttl = '1000'             # 解析记录有效生存时间TTL,单位:秒
                
                print(self.update_dns(rc_rr, rc_type, rc_value, rc_record_id, rc_ttl))
                self.write_to_file(now_ip, rc_rr)
