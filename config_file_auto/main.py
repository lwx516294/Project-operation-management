# !/usr/bin/python3
# -*- coding:utf-8 -*-
# 作者Presley
# 时间2018-11-01
# describe: 一键式生成项目信息并上传

from config_file_auto import create_jenkins
from config_file_auto import create_k8s_config_doc
from config_file_auto import create_docker_compose_config_doc
from config_file_auto import upload_config_file


def run(project_id):
    host_info={"local_host" : "192.168.30.42",
                "local_port" : 22,
                "local_user" :"root",
                "local_passwd" : "123456",

                "online_host" : "192.168.30.42",
                "online_port" : 22,
                "online_user" :"root",
                "online_passwd" : "123456"
    }
    #根据项目id创建k8s配置文件
    create_k8s_config_doc.run(project_id)

    #根据项目id创建docker-compose文件
    create_docker_compose_config_doc.run(project_id)

    #根据项目id创建jenkins信息
    jenkins = create_jenkins.Jenkins()
    jenkins.run(project_id)

    #上传配置文件
    upload_config_file.run(project_id,**host_info)

if __name__ == "__main__":
    run(11)







