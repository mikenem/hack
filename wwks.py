import requests

r = requests.get('https://api.kanye.rest/?format=text')

print (r.text)