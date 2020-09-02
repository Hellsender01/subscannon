#!/usr/bin/env python3
from dns import resolver
import requests
import threading
from queue import Queue
import os
import argparse
import time
import warnings
from bs4 import BeautifulSoup as bs

warnings.filterwarnings("ignore", category=DeprecationWarning) 

class style():
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	RESET = '\033[0m'
	MAGENTA = '\033[35m'
	UNDERLINE = '\033[4m'
	WHITE = '\033[37m'
	VOILET = '\33[36m'
	BOLD = '\033[1m'
	

print(style.BOLD)

def logo():
	print(style.BLUE+"""
   _____ __  ______ _____ _________    _   ___   ______  _   __
  / ___// / / / __ ) ___// ____/   |  / | / / | / / __ \/ | / /
  \__ \/ / / / __  \__ \/ /   / /| | /  |/ /  |/ / / / /  |/ / 
 ___/ / /_/ / /_/ /__/ / /___/ ___ |/ /|  / /|  / /_/ / /|  /  
/____/\____/_____/____/\____/_/  |_/_/ |_/_/ |_/\____/_/ |_/   
                                                               
                                            """+style.UNDERLINE+style.WHITE+"""By-Harshit Joshi
"""+style.RESET+style.BOLD+style.WHITE)

start_time = time.time()
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
def get_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t[OPTIONAL]", "--threads", dest="threads", help="Specify Threads(Default 600 (MAX - 849))")
    parser.add_argument("-d[MANDATORY]", "--domain", dest="domain", help="Specify Domain")
    parser.add_argument("-w[OPTIONAL]", "--wordlist", dest="wordlist", help="Specify Coustom Worlist To Use(Default /usr/share/subscannon/default.txt)")
    parser.add_argument("-v[OPTIONAL]", "--verbose", dest="verboses", help="For Verbose Output",nargs='?', const='')
    parser.add_argument("-f[OPTIONAL]", "--fatest", dest="fastest", help="For Fastest Output , -v -t does Not Work With Fatest Mode (Best For Large Domains)",nargs='?', const='')
    options = parser.parse_args()

    if not options.domain:
        parser.error("[+] Specify A Domain To Scan --help for more details")

    return options
    

arg = get_arg()
domain = arg.domain
threads = arg.threads
wordlist = arg.wordlist
verboses = arg.verboses
fastest = arg.fastest

queue = Queue()
subdomains = []
domains_ip = []
domain_status = []
domain_url = []
domain_title = []

dnsServer = '8.8.8.8'
ns = resolver.Resolver()
ns.nameservers = [dnsServer]

os.system("clear")

def subdomain_find(subdomain):
    hostnames = subdomain+"."+domain
    try:
        r = requests.get("https://"+hostnames,timeout=5)
        if r.status_code == 200:
            subdomains.append(hostnames)
            if fastest == "":
                pass
            else:
                domain_status.append(r.status_code)
                answers = ns.query(hostnames, "A")
                if verboses == "":
                    print("\r"+"Last Found "+style.BLUE+"➤ "+style.WHITE+hostnames,end="")                
                for ip_address in answers:
                    domains_ip.append(ip_address)
                soup = bs(r.content, 'lxml')
                domain_title.append(soup.select_one('title').text)
    except :
        pass      
    
def fill_queue(words):
  for single in words:
    queue.put(single)
    
def worker():
  while not queue.empty():
    subdomain = queue.get()
    subdomain_find(subdomain)

def check_in(string1):
    for string2 in string1.split():
        if string2.lower() in interestings:
            return True
    
if wordlist == None:
    word = open("/usr/share/subscannon/default.txt","r")
    words = word.read().splitlines()
    word.close()
else:
    word = open(wordlist,"r")
    words = word.read().splitlines()
    word.close()


fill_queue(words)

thread_list = []

logo()

if fastest == "":

	print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE + " Threads "+style.BLUE+"➤ "+style.WHITE+"870(Fastest)\n")
	for t in range(870):
		thread = threading.Thread(target=worker)
		thread_list.append(thread)

else:

	if threads:
		if int(threads) < 850:
			print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE + " Threads " +style.BLUE+"➤ "+style.WHITE+threads+"\n")
			for t in range(int(threads)):
				thread = threading.Thread(target=worker)
				thread_list.append(thread)
		if int(threads) > 849:
			print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE + " Threads "+style.BLUE+"➤ "+style.WHITE+"849(MAX)\n")
			for t in range(849):
				thread = threading.Thread(target=worker)
				thread_list.append(thread)
		  
	else:
		print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE + " Threads "+style.BLUE+"➤ "+style.WHITE+"600(Default)\n")
		for t in range(600):
		  thread = threading.Thread(target=worker)
		  thread_list.append(thread)
	 
if wordlist:
    print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE + " Wordlist "+style.BLUE+"➤ "+style.WHITE,wordlist,"\n")
else:
    print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE +" Wordlist "+style.BLUE+"➤ "+style.WHITE+"Default\n")
    
print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE +" Total Subdomains To Try "+style.BLUE+"➤"+style.WHITE,str(len(words)),"\n")

if fastest == "":
    print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE +" Verbose Mode "+style.BLUE+"➤ "+style.WHITE+"False\n")
else:
    if verboses == "":
        print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE +" Verbose Mode "+style.BLUE+"➤ "+style.WHITE+"True\n")
    else:
        print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE +" Verbose Mode "+style.BLUE+"➤ "+style.WHITE+"False\n")


if fastest == "":
    print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE +" Fastest Mode "+style.BLUE+"➤ "+style.WHITE+"True\n")
else:
    print("\n" + style.RED + "[" + style.GREEN + "+" + style.RED + "]" + style.WHITE +" Fastest Mode "+style.BLUE+"➤ "+style.WHITE+"False\n")

print("\n"+ style.MAGENTA + "{" + style.YELLOW + "#" + style.MAGENTA + "}" + style.WHITE +" Domain "+style.BLUE+"➤"+style.WHITE,style.UNDERLINE+domain+style.RESET+style.BOLD,"\n\n")

for thread in thread_list:
  thread.start()

for thread in thread_list:
  thread.join()
  
os.system("clear")

logo()

interestings = ["auth","dev","login","admin","test","lab","signin","redirect","log","sign","temp","research","labs","developer","api","working","sign in","log in","redirecting...","testing","test"]

sno = 0

if fastest == "":
    print("-"*14)
    print("| Sub-Domain |")
    print("-"*14+"\n")
    for subdom in subdomains:
        print(subdom)
        sno += 1
else:
    print("-"*133)
    print("SNO  |\tSub-Domain\t|\tIP Address     |   Status-Code  |  Interesting  |  Website Title  ")
    print("-"*133+"\n")
    for domain_ip,subdom,stat,title in zip(domains_ip,subdomains,domain_status,domain_title):
        req = check_in(title)
        ip = str(domain_ip).split(":")
        for i in ip:
            title = title.replace("\n","")
            if subdom.split(".")[0] in (string.lower() for string in interestings) or req == True:
                print("["+str(sno)+"]\r\t"+subdom,"\r\t\t\t\t"+i+"\r\t\t\t\t\t\t\t"+str(stat)+"\r\t\t\t\t\t\t\t\t   "+style.RED+"interesting\r\t\t\t\t\t\t\t\t\t\t    "+style.WHITE+(title[:49]))
            else:
                print("["+str(sno)+"]\r\t"+subdom,"\r\t\t\t\t"+i+"\r\t\t\t\t\t\t\t"+str(stat)+"\r\t\t\t\t\t\t\t\t              \r\t\t\t\t\t\t\t\t\t\t    "+(title[:49]))
        sno += 1

print("\n\nTotal Sub-Domains Found "+style.YELLOW+"{}".format(str(int(sno-1)))+style.WHITE)

end_time = time.time()

print("\nTime Taken -",str(round(end_time - start_time,1)),"Seconds","\n")
