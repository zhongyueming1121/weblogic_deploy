# coding=utf-8
# @Time    : 2021/02/04 13:48
# @Author  : ymz
# @Remark:
import getopt
import sys

# Get location of the properties file.
properties = ''
try:
    opts, args = getopt.getopt(sys.argv[1:], "p:h::", ["properies="])
except getopt.GetoptError:
    print 'create_managed_server.py -p <path-to-properties-file>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'create_managed_server.py -p <path-to-properties-file>'
        sys.exit()
    elif opt in ("-p", "--properties"):
        properties = arg
print 'properties=', properties

# Load the properties from the properties file.
from java.io import FileInputStream

propInputStream = FileInputStream(properties)
configProps = Properties()
configProps.load(propInputStream)

admin_ip = configProps.get("admin_ip")
admin_listen_port = configProps.get("admin_listen_port")
login_pwd = configProps.get("login_pwd")
login_user_name = configProps.get("login_user_name")
domain_name = configProps.get("domain_name")
weblogic_home = configProps.get("weblogic_home")

print 'admin_ip=', admin_ip
print 'admin_listen_port=', admin_listen_port
print 'login_pwd=', login_pwd
print 'login_user_name=', login_user_name
print 'domain_name=', domain_name
print 'weblogic_home=', weblogic_home

connect(str(login_user_name), str(login_pwd), 't3://' + str(admin_ip) + ':' + str(admin_listen_port))
nmEnroll(weblogic_home + "/domains/" + domain_name, weblogic_home + "/domains/" + domain_name + '/nodemanager')
disconnect()
exit()
