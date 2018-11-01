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
    host_info={"local_host" : "192.168.0.158",
                "local_port" : 22,
                "local_user" :"root",
                "local_passwd" : "d!)iW@h1N)(j",

                "online_host" : "192.168.30.42",
                "online_port" : 22,
                "online_user" :"root",
                "online_passwd" : "123456"
    }
    #根据项目id创建k8s配置文件
    print("根据项目id创建k8s配置文件".center(20,"*"))
    create_k8s_config_doc.run(project_id)
    print("配置文件创建完成".center(20,"*"))

    #根据项目id创建docker-compose文件
    print("根据项目id创建docker-compose文件".center(20,"*"))
    create_docker_compose_config_doc.run(project_id)
    print("docker-compose文件创建完成".center(20,"*"))

    #根据项目id创建jenkins信息
    print("根据项目id创建jenkins信息".center(20,"*"))
    jenkins = create_jenkins.Jenkins()
    jenkins.run(project_id)
    print("jenkins信息创建完成".center(20,"*"))

    #上传配置文件到服务器
    print("上传配置文件到服务器".center(20,"*"))
    upload_config_file.run(project_id,**host_info)
    print("上传完成".center(20,"*"))

if __name__ == "__main__":
    run(11)







