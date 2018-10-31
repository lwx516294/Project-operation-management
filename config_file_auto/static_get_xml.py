import jenkins
server = jenkins.Jenkins('http://192.168.0.156:8080', username='auto', password='pycf@123')
a = server.get_all_jobs()
print(a)
for b in a:
    print(b)