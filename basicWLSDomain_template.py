readTemplate("WEBLOGIC_HOME_T/wlserver/common/templates/wls/wls.jar")

cd('Servers/AdminServer')
set('ListenAddress', 'ADMIN_IP_T')
set('ListenPort', ADMIN_LISTEN_PORT_T)

#=======================================================================================
# Define the user password for weblogic.
#=======================================================================================

cd('/')
cd('Security/base_domain/User/weblogic')
# Please set password here before using this script, e.g. cmo.setPassword('value')
cmo.setPassword('LOGIN_PWD_T')

setOption('OverwriteDomain', 'true')

# Config home directory for the JVM to be used when starting the weblogic server
setOption('JavaHome', 'JAVA_HOME_T')

#config weblogic server run mode prod
setOption('ServerStartMode','prod') 

#=======================================================================================
# Write the domain and close the domain template.
#=======================================================================================

writeDomain('DOMAIN_HOME_T')
closeTemplate()

#=======================================================================================
# Exit WLST.
#=======================================================================================

exit()
