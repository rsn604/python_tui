import sys
if sys.version_info[0] == 2:
    from urlparse import urlparse
elif sys.version_info[0] == 3:
    from urllib.parse import urlparse

class UrlAnalyze:
    def __init__(self, url):
        parsed = urlparse(url)
        self.db_name = parsed.path[1:]
        self.username = parsed.username
        self.password = parsed.password
        self.hostname = parsed.hostname
        self.port = parsed.port
if __name__ == '__main__':
    #url = "mysql://root:test@192.168.0.28:3306/ListDB"
    url = "mysql://user01:pass01@localhost/ListDB"
    u = UrlAnalyze(url)
    print ("hostname=%s, port=%s, db_name=%s, username=%s, password=%s\n" % (u.hostname, u.port, u.db_name, u.username, u.password))

