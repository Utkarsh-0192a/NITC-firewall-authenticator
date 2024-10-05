#!/usr/bin/env python3
from pathlib import Path
import requests , argparse     #,pickle
from bs4 import BeautifulSoup
# from PIL import Image
# from io import BytesIO


home_dir= str(Path.home())

# URL of the login page
def login(user,passwd,login_url):
    # Create a session to persist cookies
    session = requests.Session()

    # Get the login page
    response = session.get(login_url)
    #save_cookies(file,session)

    if response.text=="<meta http-equiv=\"refresh\" content=\"0;url=https://support.mozilla.org/kb/captive-portal\"/>":
        print("Already logged in to NITC\nOR")
        print("Not connected to NITC network\nConnect by wifi or ethernet to login")
        print("Exiting")
        quit()
    else:
        print("Authenticating with the server")

    # Parse the login page to get any necessary hidden fields (like CSRF tokens)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the login form's input fields and action URL
    login_form = soup.find('form')
    action_url = login_form['action'] if login_form['action'].startswith('http') else login_url + login_form['action']

    # Prepare the payload (form data)
    payload = {
        'username':user,  # Replace with the actual username field name
        'password': passwd,   # Replace with the actual password field name
    }

    # Check for hidden fields and add them to the payload if necessary
    for input_tag in login_form.find_all('input'):
        if input_tag.get('type') == 'hidden':
            payload[input_tag['name']] = input_tag['value']

    # Perform the login
    login_response = session.post(action_url, data=payload)
    lnk =[]
    if login_response.ok and "logout" in login_response.text:  # Verify successful login
        print("Login successful!")
        soup = BeautifulSoup(login_response.text, 'html.parser')
        links = soup.find_all('a')  # Finds all anchor tags in the HTML
        for link in links:
            href = link.get('href')
            if href:
                lnk.append(href)
        # print(links)
    else:
        print("Login failed.")
        print("please check your username and passwprd")
        exit()

    return session,lnk

def check_website(url):
    try:
        print("checking connection to NITC network\n")
        response = requests.get(url, timeout=2)  # Send a HEAD request to minimize data transfer
        if response.status_code == 200:
            return 1
        elif response.status_code == 404:
            return 0
        else:
            return response.status_code
    except requests.RequestException:
        return 0

def logout(url1):
    if check_website(url1):
        print('Already connected. :)')
        requests.get(url1)
        print("Logged out successfully")
    else:
        print("Cannot reach the portal")
        print("Check if your pc is connected to NITC network")
        print("exiting")
        exit()
        
# def chng_passwd(url,passwd,user):
#     session = requests.Session()
#     response = session.get(url)

#     soup = BeautifulSoup(response.content, 'html.parser')

#     form=soup.find("form")
#     captcha_img = form.find('img', {'id': 'captcha_image'})  # Replace with actual id/class
#     if captcha_img:
#         captcha_url = captcha_img['src']
#         if captcha_url.startswith('/'):
#             captcha_url = login_page_url + captcha_url  # Construct full URL
        
#         captcha_response = session.get(captcha_url)
#         if captcha_response.status_code == 200:
#             img = Image.open(BytesIO(captcha_response.content))
#             img.save("captcha_image.png")  # Save the CAPTCHA image
#             img.show()  # Show the image to the user
            
#             captcha_solution = input("Please enter the CAPTCHA text: ")

#             login_data = {
#             'username': user,  # Replace with actual username field name
#             'password': passwd,  # Replace with actual password field name
#             'captcha': captcha_solution,    # Add the CAPTCHA solution here
#         }





# def save_cookies(file,session):

#     with open(file, 'wb') as f:
#         pickle.dump(session.cookies, f)


# # Function to load cookies 
# def load_cookies(file):
#     # Start a session
#     session = requests.Session()

#     # Load cookies from file
#     try:
#         with open(file, 'rb') as f:
#             session.cookies.update(pickle.load(f))
#         print("Cookies loaded successfully!")
#     except FileNotFoundError:
#         print("No cookies file found. Please log in first.")

#         return session

def getdefaultpass():
    cred =[]
    with open(home_dir+"/Authenticator/credential.txt",'r') as fl:
        for ln in fl:
            cred.append(ln.strip())
        fl.close()
    return cred[0],cred[1]


def updatecred(user,pas):

    with open(home_dir+"/Authenticator/credential.txt",'w') as fl:
        fl.write(user+"\n")
        fl.write(pas+"\n")
        print("credential are succesfuly updated")
        fl.close()


def updatelinks(ln):
    with open(home_dir+"/Authenticator/links.txt",'w') as fl:
        fl.write(ln[2]+"\n")
        fl.write(ln[1]+"\n")
        fl.close()       

def getlinks():
    lin=[]
    with open(home_dir+"/Authenticator/links.txt",'r') as fl:
        for lnk in fl:
            lin.append(lnk.strip())
        fl.close()
    return lin[0],lin[1]


if __name__ == '__main__':


    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--login", help = "login to network",action='store_true')
    parser.add_argument("-lo", "--logout", help = "logout of the network",action='store_true')
    parser.add_argument("-u", "--user", help = "username to login")
    parser.add_argument("-p", "--passwd", help = "password to login")
    parser.add_argument("-cd", "--chngdefaultuser", help = "change default user passwd saved for login",action='store_true')
    #parser.add_argument("-c", "--chngpass", help = "change password for the user enter new passwd")
    parser.add_argument("-s", "--shutlo", help =argparse.SUPPRESS,action='store_true')
    
    args= parser.parse_args()
    if not any(vars(args).values()):
        parser.print_help()
        parser.exit()
    
    flag1=True
    flag2=False
    if args.shutlo:
        logout(getlinks[0])

    if args.chngdefaultuser:
        usernm =args.user
        password=args.passwd
        flag1=False
        updatecred(usernm,password)

    if flag1:
        if args.user:
            usernm = args.user
            password = args.passwd
            print("Using username: ",usernm)
        else:
            usernm,password=getdefaultpass()

    if args.login:
        l_url = "http://detectportal.firefox.com/canonical.html"
        ses,links=login(usernm,password,l_url)
        flag2=True
        updatelinks(links)
        #print(links)

    # if args.logout | args.chngpass:
    #     if not flag2:
    #         lgot_lnk,chnglink=getlinks()
        
    if args.logout:
        if flag2:
            logout(links[2])
        else:
            lgot_lnk,chnglink=getlinks()
            logout(lgot_lnk)


    # chnglink="http://192.168.200.126/REGISTRATION/pwd.php"
    # if args.chngpass:
    #     if flag2:
    #         chng_passwd(links[1],args.chngpass)
    #     else:
    #         chng_passwd(chnglink,args.chngpass)
        
