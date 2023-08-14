import requests
import queue
import threading
import sys
import time
import argparse
import argparse
from colorama import Fore

Yellow = Fore.YELLOW
Green = Fore.GREEN
Red = Fore.RED
Blue = Fore.BLUE
Reset = Fore.RESET

Threads = 50
StatusCodeFilter = ""
log = open("log.txt", "a", encoding="gbk")


# 单url dic字典
# 单url 单dic
# 多url 单dic
# 多url dic字典
# get_url，输入url文件，返回一个url序列
# 单url 单路径,输入url，路径，报文类型，返回结果
def url_dic(url, dic, request_type):
    path = url + dic
    status_code, resp_len, path = send_request(path, request_type)
    if not StatusCodeFilter:
        printfunc(status_code, resp_len, path)
    elif status_code == StatusCodeFilter:
        printfunc(status_code, resp_len, path)
    else:
        pass
    # result = ("[%s]\t%s\t%s" % (status_code, resp_len, path))
    # print(result)


# 多url 单路径
def urls_dic(urlfile, dic, request_type):
    threads = []
    path_queue = get_urls(urlfile, dic)
    for i in range(Threads):
        t = threading.Thread(target=thread_run, args=(path_queue, request_type,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


# 单url 多路径,输入url，dic字典，报文类型
def url_dics(url, dicfile, request_type):
    # 拼接字典，返回url序列
    # print(dicfile)
    threads = []
    path_queue = get_dics(url, dicfile)
    for i in range(Threads):
        t = threading.Thread(target=thread_run, args=(path_queue, request_type,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


# 多url，多路径,输入url字典，dic字典，报文类型
def urls_dics(urlfile, dicfile, request_type):
    # print(urlfile, dicfile, request_type)
    url_list = []
    # 打开文件
    f = open(urlfile, "r", encoding="gbk")
    for i in f.readlines():
        url_list.append(i.strip())
    for j in url_list:
        print("start scan URL:", j)
        url_dics(j, dicfile, request_type)


# 输出打印函数，对状态码等进行颜色变换
def printfunc(status_code, resp_len, path):
    status = str(status_code)[:1]
    if status == "4":
        result = f"{Red}{status_code}{Reset}\t{resp_len}\t{path}"
    elif status == "3":
        result = f"{Blue}{status_code}{Reset}\t{resp_len}\t{path}"
    elif status == "2":
        result = f"{Green}{status_code}{Reset}\t{resp_len}\t{path}"
    elif status == "5":
        result = f"{Red}{status_code}{Reset}\t{resp_len}\t{path}"
    else:
        result = f"{status_code}\t{resp_len}\t{path}"
    print(result)
    log.write(repr(f"{status_code} {resp_len} {path}").replace("\'", ""))
    log.write("\n")


# 多线程跑字典
def thread_run(path_queue, request_type):
    while not path_queue.empty():
        # threadname = threading.current_thread().name
        try:
            status_code, resp_len, path = send_request(path_queue.get(), request_type)
            # result = f"{Yellow}{status_code}{Reset}\t{resp_len}\t{path}"
            if not StatusCodeFilter:
                printfunc(status_code, resp_len, path)
            elif status_code == StatusCodeFilter:
                printfunc(status_code, resp_len, path)
            else:
                pass
            # printfunc(status_code, resp_len, path)
            # print(result)
        except:
            pass


# 获取url字典，返回一个URL字典序列
def get_urls(urlfile, dic):
    path_queue = queue.Queue()
    # 打开文件
    f = open(urlfile, "r", encoding="gbk")
    for i in f.readlines():
        path = get_path(i.strip(), dic)
        path_queue.put(path)
    f.close()
    return path_queue


# 获取路径，输入url和字典文件，返回一个字典序列
def get_dics(url, dicfile):
    path_queue = queue.Queue()
    # 打开文件
    f = open(dicfile, "r", encoding="gbk")
    for i in f.readlines():
        path = get_path(url, i.strip())
        path_queue.put(path)
    f.close()
    return path_queue


# 定义路径获取urldic,输入url，字典路径，返回拼接内容
def get_path(url, dic):
    return url + dic


# request请求,输入路径，返回状态码，路径，报文长度
def send_request(url, request_type):
    resp = requests.models.Response()
    try:
        if request_type == "head":
            resp = requests.head(url, timeout=5)
        elif request_type == "get":
            resp = requests.get(url, timeout=5)
        elif request_type == "post":
            resp = requests.post(url, timeout=5)
        if (resp.status_code == 302) or (resp.status_code == 301):
            # url = (url, "\t", resp.status_code, "jump->", resp.headers.get("Location"))
            url = "[%s]\t%djump-> [%s]" % (url, resp.status_code, resp.headers.get("Location"))
        return resp.status_code, "[len:%d]" % len(resp.text), "%s" % url
    except:
        pass


def display_banner():
    banne_text = rbanne_text = r"""
  ▄████  ██▀███   ███▄ ▄███▓
 ██▒ ▀█▒▓██ ▒ ██▒▓██▒▀█▀ ██▒    G3forDirscan
▒██░▄▄▄░▓██ ░▄█ ▒▓██    ▓██░    
░▓█  ██▓▒██▀▀█▄  ▒██    ▒██     Coded By G3RM4
░▒▓███▀▒░██▓ ▒██▒▒██▒   ░██▒    
 ░▒   ▒ ░ ▒▓ ░▒▓░░ ▒░   ░  ░    Ice technology
  ░   ░   ░▒ ░ ▒░░  ░      ░
░ ░   ░   ░░   ░ ░      ░       https[:]//github.com/mengmeng9921/PocTest
      ░    ░            ░       tips:XXX                                
"""
    print(f"{Yellow}{banne_text}{Reset}")


# 接收命令行参数
def cmdline(known=False):
    parser = argparse.ArgumentParser(description=display_banner())
    parser.add_argument(
        '-u',
        '--url',
        help='-u http://test.com',
        type=str
    )
    parser.add_argument(
        '-uf',
        '--urlfile',
        help='-uf 1.txt',
        type=str
    )
    parser.add_argument(
        '-d',
        '--dic',
        help='-d "/index.php"',
        type=str
    )
    parser.add_argument(
        '-df',
        '--dicfile',
        help='-df 1.txt',
        default="dicc.txt",
        type=str
    )
    parser.add_argument(
        '-t',
        '--threads',
        help='-t 10',
        default=50,
        type=int
    )
    parser.add_argument(
        '-r',
        '--requestype',
        help='-r get',
        default="head",
        type=str
    )
    parser.add_argument(
        '-sf',
        '--statuscodefilter',
        help='-sf 200',
        default= None,
        type=int
    )
    opt = parser.parse_args()
    return opt


# 主函数
def main():
    global Threads
    global StatusCodeFilter
    opt = cmdline()
    Threads = opt.threads
    StatusCodeFilter = opt.statuscodefilter
    # 1.没有单个路径
    if not opt.dic:
        # 1.1 没有url字典
        if not opt.urlfile:
            url_dics(opt.url, opt.dicfile, opt.requestype)
        # 1.2 有url字典
        elif opt.urlfile:
            urls_dics(opt.urlfile, opt.dicfile, opt.requestype)
        # 1.3 参数错误，退出
        else:
            print("参数错误")
            sys.exit()
    # 2.有单个路径
    elif opt.dic:
        # 2.1 没有url字典
        if not opt.urlfile:
            url_dic(opt.url, opt.dic, opt.requestype)
        # 2.2 有url字典
        elif opt.urlfile:
            urls_dic(opt.urlfile, opt.dic, opt.requestype)
        # 2.3 参数错误，退出
        else:
            print("参数错误")
            sys.exit()
    else:
        print("参数错误")
        sys.exit()
    log.close()


if __name__ == '__main__':
    main()
