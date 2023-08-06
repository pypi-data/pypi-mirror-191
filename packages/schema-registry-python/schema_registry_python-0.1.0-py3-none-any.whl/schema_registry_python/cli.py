from httpx import get

def cli():
            print( get('http://httpbin.org/get?args=Live de Python').json()['args']['arg'])