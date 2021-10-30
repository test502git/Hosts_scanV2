# -*- coding: UTF-8 -*-
#Author:tangshpupu 
#这是一个用于IP和域名碰撞匹配访问的小工具升级版
import itertools
import signal
import threading
from multiprocessing.dummy import Pool
from time import sleep

from requests.packages import chardet
import requests
import re
from lib.processbar import ProcessBar


def host_check(host_ip):
    host,ip = host_ip
    schemes = ["http://","https://"]
    for scheme in schemes:
        url = scheme+ip
        headers = {'Host':host.strip(),'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        try:
            r = requests.session()
            requests.packages.urllib3.disable_warnings()
            res = r.get(url,verify=False,headers=headers,timeout=30)
            charset = chardet.detect(res.content)["encoding"]
            res.encoding = charset
            title = ""
            try:
                title = re.search('<title>(.*)</title>', res.text).group(1) #获取标题
            except Exception as ex:
                title = u"获取标题失败"
            info = u'%s\t%s -- %s 数据包大小：%d 标题：%s' % (ip,host,scheme+host,len(res.text),title)
            if lock.acquire():
                try:
                    success_list.append(info)
                    pbar.echo(info)
                    pbar.update_suc()
                    open('hosts_ok-ism.txt','a', encoding='utf-8').write(str(info)+'\n')
                    with open('hosts_ok.txt','a+') as f:
                        f.write(info.encode("utf-8") + "\n")
                        f.close()

                finally:
                    lock.release()

        except Exception as ex:
            if lock.acquire():
                try:
                    # print ex.message
                    # logging.exception(ex)
                    error = u"%s\t%s -- %s  访问失败！~" % (ip,host, scheme+host)
                    pbar.echo(error)
                finally:
                    lock.release()
        finally:
            pbar.update()



if __name__ == '__main__':
    lock = threading.Lock()
    success_list = []
    ip_list = open("ip.txt").read().splitlines()
    host_list = open("host.txt").read().splitlines()
    host_ip_list = list(itertools.product(host_list,ip_list))

    print(u"====================================开 始 匹 配====================================")

    pbar = ProcessBar(len(host_ip_list))

    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGINT, original_sigint_handler)

    pool = Pool(40)

    try:
        pool.map_async(host_check, host_ip_list)
        while not pbar.cur_cnt==pbar.total:
            sleep(10)

    except KeyboardInterrupt:
        pbar.echo(u"结束子线程中...")
        pool.terminate()
        pool.close()

    else:
        pool.close()
        pool.join()

    pbar.close()


    print(u"====================================匹 配 成 功 的 列 表====================================")
    for i in success_list:
        print(i)

