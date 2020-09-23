from net_auth import net_auth
import aliyun_ddns
import yaml
import os
from time import sleep

with open(r'setting.yaml','r',encoding='UTF-8') as f:
    s = yaml.safe_load(f)
    print(yaml.dump(s,default_flow_style=False))
    
# 阿里云 Access Key ID
access_key_id = s['access_key_id']
# 阿里云 Access Key Secret
access_key_secret = s['access_key_secret']
# 阿里云 一级域名
rc_domain = s['rc_domain']
# 解析记录
rc_rr_list = s['rc_rr_list']

netauth_addr = s['netauth_addr']
netauth_nanme = s['netauth_nanme']
netauth_passwd = s['netauth_passwd']
ping_addr = s['ping_addr']
cmd = 'ping ' + ping_addr
def check_netstatus(addr):
    return  os.system(cmd)


if __name__ == '__main__':
    ddns = aliyun_ddns.aliyun_ddns(access_key_id,access_key_secret,rc_domain,rc_rr_list)
    ip = net_auth(netauth_addr,netauth_nanme,netauth_passwd)
    ddns.ddns(ip)
    while True:
        if check_netstatus(ping_addr):
            print("网络错误，15秒后再次尝试")
            ip = net_auth(netauth_addr,netauth_nanme,netauth_passwd)
            ddns.ddns(ip)
        sleep(600)

