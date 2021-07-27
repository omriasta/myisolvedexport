import requests
from bs4 import BeautifulSoup
from const import USERNAME, PASSWORD, TOKEN, TOKEN_EXPIRATION


def Authentication():

    s = requests.Session()
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'Origin': 'https://accudata.myisolved.com',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://accudata.myisolved.com/SecurityVerification.aspx?r=sms&u=&ReturnUrl=%2f',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    s.headers = headers

    login_0 = s.get("https://accudata.myisolved.com/UserLogin.aspx?ReturnUrl=%2f")
    soup = BeautifulSoup(login_0.content, 'html5lib')
    data = {}
    for tag in soup.select('input[name^=ctl00]'):
        if tag.get('value'):
            key, value = tag['name'], tag['value']
            data[key] = value
        else:
            key = tag['name']
            data[key] = ''

    state = { 
        tag['name']: tag['value'] 
            for tag in soup.select('input[name^=__]')
    }
    data.update(state)
    params = (
        ('ReturnUrl', '/'),
    )

    data['ctl00$NoBot1$NoBot1_NoBotExtender_ClientState'] = '-243'
    data['ctl00$DefaultContent$Login1$UserName'] = USERNAME
    data['ctl00$DefaultContent$Login1$Button1'] = 'Continue'
    data['ctl00_ToolkitScriptManager1_HiddenField'] = ''

    response = s.post('https://accudata.myisolved.com/UserLogin.aspx', params=params, data=data)
    soup = BeautifulSoup(response.content, 'html5lib')
    data = {}
    for tag in soup.select('input[name^=ctl00]'):
        if tag.get('value'):
            key, value = tag['name'], tag['value']
            data[key] = value
        else:
            key = tag['name']
            data[key] = ''

    state = { 
        tag['name']: tag['value'] 
            for tag in soup.select('input[name^=__]')
    }
    data.update(state)
    params = (
        ('ReturnUrl', '/'),
    )

    data['ctl00$DefaultContent$Login1$UserName'] = USERNAME
    data['ctl00$DefaultContent$Login1$Password'] = PASSWORD
    data['ctl00$DefaultContent$Login1$Login'] = 'Login'
    data['ctl00_ToolkitScriptManager1_HiddenField'] = ''
    data['ctl00$NoBot1$NoBot1_NoBotExtender_ClientState'] = ''
    data.pop('ctl00$DefaultContent$Login1$Cancel', None)
    response = s.post('https://accudata.myisolved.com/UserLogin.aspx', params=params, data=data)

    params = (
        ('ReturnUrl', '/'),
    )

    response = s.get('https://accudata.myisolved.com/GetAuthorizationCode.aspx?ReturnUrl=%2f', params=params)

    params = (
        ('ReturnUrl', '/'),
    )
    soup = BeautifulSoup(response.content, 'html5lib')
    data = {}
    for tag in soup.select('input[name^=ctl00]'):
        if tag.get('value'):
            key, value = tag['name'], tag['value']
            data[key] = value
        else:
            key = tag['name']
            data[key] = ''

    state = { 
        tag['name']: tag['value'] 
            for tag in soup.select('input[name^=__]')
    }
    data.update(state)

    data['ctl00$NoBot1$NoBot1_NoBotExtender_ClientState'] = '-394'
    data['ctl00$DefaultContent$AuthCodeDeliveryMethodGroup'] = 'AuthCodeSMSSelect'
    data['ctl00$DefaultContent$GetAuthCodeButton'] = 'Get Authorization Code'
    data['ctl00_defaultScriptManager_HiddenField'] = ''

    response = s.post('https://accudata.myisolved.com/GetAuthorizationCode.aspx?ReturnUrl=%2f', params=params, data=data)

    params = (
        ('r', 'sms'),
        ('u', ''),
        ('ReturnUrl', '/'),
    )

    response = s.get('https://accudata.myisolved.com/SecurityVerification.aspx', params=params)
    print("Enter Auth Code:")
    authcode = input()
    params = (
        ('r', 'sms'),
        ('u', ''),
        ('ReturnUrl', '/'),
    )
    soup = BeautifulSoup(response.content, 'html5lib')
    data = {}
    for tag in soup.select('input[name^=ctl00]'):
        if tag.get('value'):
            key, value = tag['name'], tag['value']
            data[key] = value
        else:
            key = tag['name']
            data[key] = ''

    state = { 
        tag['name']: tag['value'] 
            for tag in soup.select('input[name^=__]')
    }
    data.update(state)

    data['ctl00$NoBot1$NoBot1_NoBotExtender_ClientState'] = '-46'
    data['ctl00$DefaultContent$AuthCodeTextBox'] = authcode
    data['ctl00$DefaultContent$LoginButton'] = 'Login'
    data['ctl00_defaultScriptManager_HiddenField'] = ''
    response = s.post('https://accudata.myisolved.com/SecurityVerification.aspx', params=params, data=data)


    expires = next(x for x in s.cookies if x.name == 'iSolvedDeviceToken').expires
    value = next(x for x in s.cookies if x.name == 'iSolvedDeviceToken').value
    file = open("const.py", "w")
    file.write(
        "USERNAME = \"" + str(USERNAME) + "\"" "\n"
        "PASSWORD = \"" + str(PASSWORD) + "\"" "\n"
        "TOKEN = \"" + str(value) + "\"" "\n"
        "TOKEN_EXPIRATION = " + str(expires) + "\n"
    )
    file.close
    return value