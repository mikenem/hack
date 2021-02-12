import requests
import json
import getpass
from requests.auth import AuthBase

authtoken = getpass.getpass(prompt='Enter authentication token: ')

loops = int(input("How many times should this run?"))

cycle = 0

while cycle < loops:

    i = 0

    r = requests.get('https://randomuser.me/api/?results=100&inc=name,gender,nat,email,location,id&noinfo')
    f = open("o_contact.json", "w")
    f.write("[ ")
    f.close
    # Extract field values
    while i < 100 :  
        users = json.loads(r.text)
        results = users["results"][i]
        gender = results["gender"]
        name_array = results["name"]
        first = name_array["first"]
        last = name_array["last"]
        title = name_array["title"]
        email = results["email"]
        id_array = results["id"]
        customer_id = (id_array["value"])

    # put them back in an Ometria formatted object

        contact_object = {
            "@type": "contact",
            "id": customer_id,
            "email": email,
            "firstname": first,
            "lastname": last,
            "prefix": title,
            "gender": gender,
            "timestamp_acquired": "2015-01-02T09:00:00+00" # should eventually grab current tstamp
        }

    # write to a file
        write_object = json.dumps(contact_object)
        f = open("o_contact.json", "a")
        f.write(write_object)
        if i < 99:
            f.write(",")    
        f.close
        i += 1

    # send to Ometria push api
    f = open("o_contact.json", "a")
    f.write(" ]")
    f.close
    print(i)
    # adding this little doo-hicky to deal with Ometria's custom auth header
    class OmetriaAuth(AuthBase):
        """Attaches HTTP Ometria Authentication to the given Request object."""
        def __init__(self, token):
            # setup any auth-related data here
            self.token = token

        def __call__(self, p):
            # modify and return the request
            p.headers['X-Ometria-Auth'] = self.token
            return p


    url = 'https://api.ometria.com/v2/push'
    headers = {
            'Content-Type': 'application/json'
            } 
    
    data = open('o_contact.json', 'r').read()

    payload = data + " ]"
    # print(data + " ]")

    p = requests.post(url=url, data=(data + " ]"), headers=headers, auth=OmetriaAuth(authtoken))
    """ f2 = open("user-gen-output.txt", "a")
    f2.write(p.response)
    f2.close """
    print (p.responses)

    cycle += 1