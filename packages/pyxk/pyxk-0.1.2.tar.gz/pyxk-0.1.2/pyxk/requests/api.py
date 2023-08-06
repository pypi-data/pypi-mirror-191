"""
requests api
"""
from pyxk.requests import sessions



def request(method, url, **kwargs):
    """
    Usage:

      >>> import pyxk
      >>> resp = pyxk.request('GET', 'http://www.baidu.com')
      >>> resp
      <Response [200]>
    """
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)

def get(url, params=None, **kwargs):
    return request("GET", url, params=params, **kwargs)

def options(url, **kwargs):
    return request("OPTIONS", url, **kwargs)

def head(url, allow_redirects=False, **kwargs):
    return request("HEAD", url, allow_redirects=allow_redirects, **kwargs)

def post(url, data=None, json=None, **kwargs):
    return request("POST", url, data=data, json=json, **kwargs)

def put(url, data=None, **kwargs):
    return request("PUT", url, data=data, **kwargs)

def patch(url, data=None, **kwargs):
    return request("PATCH", url, data=data, **kwargs)

def delete(url, **kwargs):
    return request("DELETE", url, **kwargs)


if __name__=="__main__":

    resp = get("http://www.baidu.com")
    print(resp)
