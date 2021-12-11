# coding=utf-8
# @Time    : 2021/02/04 09:37
# @Author  : ymz
# @Remark: 一键安装weblogic
import os
import subprocess
import sys
import time


class Properties(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.properties = {}

    def __getDict(self, strName, dictName, value):
        if (strName.find('.') > 0):
            k = strName.split('.')[0]
            dictName.setdefault(k, {})
            return self.__getDict(strName[len(k) + 1:], dictName[k], value)
        else:
            dictName[strName] = value
            return

    def getProperties(self):
        try:
            pro_file = open(self.fileName, 'Ur')
            for line in pro_file.readlines():
                line = line.strip().replace('\n', '')
                if line.find("#") != -1:
                    line = line[0:line.find('#')]
                if line.find('=') > 0:
                    strs = line.split('=')
                    strs[1] = line[len(strs[0]) + 1:]
                    self.__getDict(strs[0].strip(), self.properties, strs[1].strip())
        except Exception, e:
            raise e
        else:
            pro_file.close()
        return self.properties


def load_config():
    current_path = os.path.abspath(__file__)
    file_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    dict_properties = Properties(file_path + "/info.properties").getProperties()
    return dict_properties


pr = load_config()
admin_ip = pr["admin_ip"]
run_mode = pr["run_mode"]
admin_listen_port = pr["admin_listen_port"]
login_pwd = pr["login_pwd"]
login_user_name = pr["login_user_name"]
inst_user = pr["inst_user"]
java_home = pr["java_home"]
domain_name = pr["domain_name"]
weblogic_home = pr["weblogic_home"]
my_ip = pr["my_ip"]
my_port = pr["my_port"]
nm_port = pr["nm_port"]
domain_home = weblogic_home + "/domains/" + domain_name
# 要安装的weblogic安装包
fmw_jar_file_name = "fmw_12.2.1.3.0_wls.jar"

print "admin_ip =" + admin_ip
print "run_mode =" + run_mode
print "admin_listen_port =" + admin_listen_port
print "login_pwd =" + login_pwd
print "login_user_name =" + login_user_name
print "inst_user =" + inst_user
print "java_home =" + java_home
print "domain_name =" + domain_name
print "weblogic_home =" + weblogic_home
print "my_ip =" + my_ip
print "my_port =" + my_port
print "nm_port =" + nm_port
print "domain_home =" + domain_home

_WEBLOGIC_HOME = weblogic_home
_JDK_HOME = java_home
_MY_IP = my_ip
_NM_PORT = nm_port

_FILE_PATH = ""


def load_path():
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    print('path:%s' % father_path)
    global _FILE_PATH
    _FILE_PATH = father_path
    print "_FILE_PATH =" + _FILE_PATH


def replace_args():
    file_path_str = _FILE_PATH + '/basicWLSDomain_template.py ' + _FILE_PATH + '/boot.properties ' \
                    + _FILE_PATH + '/oraInst.loc ' + _FILE_PATH + '/wls.rsp '
    sed_cmd1 = 'sed -i "s?ADMIN_IP_T?' + admin_ip + '?g" ' + file_path_str
    sed_cmd2 = 'sed -i "s?ADMIN_LISTEN_PORT_T?' + admin_listen_port + '?g" ' + file_path_str
    sed_cmd3 = 'sed -i "s?LOGIN_PWD_T?' + login_pwd + '?g" ' + file_path_str
    sed_cmd4 = 'sed -i "s?LOGIN_USER_NAME_T?' + login_user_name + '?g" ' + file_path_str
    sed_cmd5 = 'sed -i "s?INST_USER_T?' + inst_user + '?g" ' + file_path_str
    sed_cmd6 = 'sed -i "s?JAVA_HOME_T?' + java_home + '?g" ' + file_path_str
    sed_cmd7 = 'sed -i "s?DOMAIN_HOME_T?' + domain_home + '?g" ' + file_path_str
    sed_cmd8 = 'sed -i "s?DOMAIN_NAME_T?' + domain_name + '?g" ' + file_path_str
    sed_cmd9 = 'sed -i "s?WEBLOGIC_HOME_T?' + weblogic_home + '?g" ' + file_path_str
    sed_cmd10 = 'sed -i "s?TMP_FILE_HOME_T?' + _FILE_PATH + '?g" ' + file_path_str

    cmd_exec(sed_cmd1)
    cmd_exec(sed_cmd2)
    cmd_exec(sed_cmd3)
    cmd_exec(sed_cmd4)
    cmd_exec(sed_cmd5)
    cmd_exec(sed_cmd6)
    cmd_exec(sed_cmd7)
    cmd_exec(sed_cmd8)
    cmd_exec(sed_cmd9)
    cmd_exec(sed_cmd10)


def create_domain():
    """
    创建域
    :return:
    """
    print "开始创建域..."
    cmd = _WEBLOGIC_HOME + "/oracle_common/common/bin/wlst.sh " + _FILE_PATH + "/basicWLSDomain_template.py"
    cmd_exec(cmd)
    print "创建域完成"


def set_admin_server():
    """
    配置adminserver
    :return:
    """
    print "开始设置AdminServer..."
    boot_pr_path = domain_home + "/servers/AdminServer/security"
    if not os.path.exists(boot_pr_path):
        os.makedirs(boot_pr_path)
    # 复制免密登录文件
    cmd = "cp " + _FILE_PATH + "/boot.properties " + boot_pr_path
    cmd_exec(cmd)
    # 配置初始jvm大小
    sed_jvm_cmd = 'sed -i "s/-Xms512m -Xmx512m/-Xms1024m -Xmx1024m/g" ' + domain_home + '/bin/setDomainEnv.sh ' \
                  + '&& sed -i "s/-Xms256m -Xmx512m/-Xms1024m -Xmx1024m/g" ' + domain_home + '/bin/setDomainEnv.sh'
    cmd_exec(sed_jvm_cmd)
    # 启动AdminServer
    print "开始启动AdminServer..."
    start_server_cmd = "nohup " + domain_home + "/bin/startWebLogic.sh &> /dev/null &"
    cmd_exec(start_server_cmd)
    print "结束设置AdminServer..."


def set_nodeManager():
    """
    配置节点管理器
    :return:
    """
    _nmEnroll()
    print "开始替换nodemanager配置..."
    # 修改配置文件
    nodemanager_pr_file = domain_home + "/nodemanager/nodemanager.properties"
    sed_listen_ip_cmd = 'sed -i "s#ListenAddress=localhost#ListenAddress=' + _MY_IP + '#g" ' + nodemanager_pr_file
    sed_listen_port_cmd = 'sed -i "s#ListenPort=5556#ListenPort=' + _NM_PORT + '#g" ' + nodemanager_pr_file
    sed_SecureListener_cmd = 'sed -i "s#SecureListener=true#SecureListener=false#g" ' + nodemanager_pr_file
    cmd_exec(sed_listen_ip_cmd)
    cmd_exec(sed_listen_port_cmd)
    cmd_exec(sed_SecureListener_cmd)
    print "结束替换nodemanager配置..."
    _start_nodeManager()


def _nmEnroll():
    """
    注册节点
    :return:
    """
    server_up = _check_admin_server()
    if str(server_up) not in "1":
        print "连接AdminServer错误，AdminServer未启动!!!"
        exit()
    print "开始注册nodemanager..."
    cmd = "source " + domain_home + "/bin/setDomainEnv.sh && java weblogic.WLST " + _FILE_PATH + "/run_wlst.py -p " \
          + _FILE_PATH + "/info.properties"
    cmd_exec(cmd)
    print "完成注册nodemanager..."


def _check_admin_server():
    """
    判断admin服务是否启动
    """
    url = 'http://' + str(admin_ip) + ':' + str(admin_listen_port) + '/console'
    cmd = 'curl -L ' + url + ' | grep -Eo "Oracle WebLogic Server"'
    print "check adminServer status..."
    print cmd
    for i in range(1, 18):
        exec_return = cmd_exec_return(cmd)
        if "Oracle WebLogic Server" in str(exec_return):
            return "1"
        else:
            print '{0}'.format("."),
            time.sleep(10)
    return "0"


def cmd_exec_return(cmd):
    """
    执行命令
    :param cmd:
    :param mybk
    :return:
    """
    # print ("执行shell:%s" % str(cmd))
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    data = p.stdout.read()
    ret = str(data)
    return ret


def _start_nodeManager():
    """
    启动nodemanger
    :return:
    """
    print "开始启动nodemanager..."
    cmd = "nohup " + domain_home + "/bin/startNodeManager.sh &> /dev/null &"
    cmd_exec(cmd)
    print "完成启动nodemanager..."


def create_weblogic():
    """
    安装weblogic
    :return:
    """
    print "开始安装weblogic..."
    cmd = _JDK_HOME + "/bin/java -jar " + _FILE_PATH + "/" + fmw_jar_file_name + " -silent -responseFile " \
          + _FILE_PATH + "/wls.rsp -invPtrLoc " + _FILE_PATH + "/oraInst.loc ORACLE_HOME=" + _WEBLOGIC_HOME
    cmd_exec(cmd)
    print "安装weblogic完成"


def cmd_exec(cmd):
    """
    执行命令
    :param cmd:
    :return:
    """
    print ("执行shell:%s" % str(cmd))
    cmd = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=sys.stderr, close_fds=True,
                           stdout=sys.stdout, universal_newlines=True, shell=True, bufsize=1)
    cmd.communicate()
    print "shell 执行结果:" + str(cmd.returncode)
    if cmd.returncode is not 0:
        print "shell 执行错误，程序退出"
        exit()
    return cmd.returncode


def load_config():
    dict_properties = Properties(_FILE_PATH + "/info.properties").getProperties()
    return dict_properties


def run_mode1():
    """
    创建管理节点
    :return:
    """
    replace_args()
    create_weblogic()
    create_domain()
    set_admin_server()


def run_mode2():
    """
    创建节点管理器
    :return:
    """
    replace_args()
    create_weblogic()
    create_domain()
    set_nodeManager()


def run_mode3():
    """
    创建管理节点和节点管理器
    :return:
    """
    replace_args()
    create_weblogic()
    create_domain()
    set_admin_server()
    set_nodeManager()


if __name__ == '__main__':
    load_path()
    if "" == _FILE_PATH:
        print "error file path is null,exit!!"
        exit()
    # only adminServer
    if run_mode == "1":
        run_mode1()
    # only mServer
    if run_mode == "2":
        run_mode2()
    # adminServer and mServer
    if run_mode == "3":
        run_mode3()
