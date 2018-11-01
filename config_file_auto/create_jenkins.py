import os
import jenkins
from config_file_auto.config.settings import *
from jinja2 import Environment, FileSystemLoader

class Jenkins:
    def __init__(self):
        self.server = jenkins.Jenkins('http://192.168.0.156:8080', username='auto', password='pycf@123')
        self.modules = list()

    #创建job的配置文件
    @staticmethod
    def _create_jenkins_config_xml(project_name, module_name, svn_address, dev_port, pro_port, harbor_url):
        env = Environment(loader=FileSystemLoader(searchpath='./templates'))
        template = env.get_template('jenkins-template.xml.j2')
        config_xml = template.render(project_name=project_name, module_name=module_name, svn_address=svn_address,
                                     dev_port=dev_port, pro_port=pro_port, harbor_url=harbor_url)

        dir_name = "{project_name}/jenkins/".format(project_name=project_name, )
        file_name = "{project_name}-{module_name}.xml".format(project_name=project_name, module_name=module_name)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file = "{dir_name}/{file_name}".format(dir_name=dir_name, file_name=file_name)
        with open(file, 'w') as conf_file:
            conf_file.write(config_xml)
            return config_xml

    #创建python job的配置文件
    @staticmethod
    def _create_jenkins_python_config_xml(project_name, module_name, svn_address, dev_port, pro_port, harbor_url,python_image = None):
        env = Environment(loader=FileSystemLoader(searchpath='./templates'))
        template = env.get_template('jenkins-python-template.xml.j2')
        config_xml = template.render(project_name=project_name, module_name=module_name, svn_address=svn_address,
                                     dev_port=dev_port, pro_port=pro_port, harbor_url=harbor_url,python_image = python_image)

        dir_name = "{project_name}/jenkins/".format(project_name=project_name)
        file_name = "{project_name}-{module_name}.xml".format(project_name=project_name, module_name=module_name)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file = "{dir_name}/{file_name}".format(dir_name=dir_name, file_name=file_name)
        with open(file, 'w') as conf_file:
            conf_file.write(config_xml)
            return config_xml

    # 创建静态资源的job配置文件
    @staticmethod
    def _create_jenkins_staticresource_config_xml(project_name,module_name,svn_address):
        env = Environment(loader=FileSystemLoader(searchpath='./templates'))
        template = env.get_template('jenkins-staticresource-template.xml.j2')
        config_xml = template.render(project_name = project_name,module_name = module_name,svn_address = svn_address)
        dir_name = "{project_name}/jenkins/".format(project_name=project_name)
        file_name = "{project_name}-{module_name}.xml".format(project_name=project_name, module_name=module_name)
        file = "{dir_name}/{file_name}".format(dir_name=dir_name, file_name=file_name)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(file, 'w') as conf_file:
            conf_file.write(config_xml)
            return config_xml
    #创建job
    def _create_jenkins_job(self, job_name, config_xml):
        exist = self.server.get_job_name(job_name)
        if not exist:
            self.server.create_job(job_name, config_xml)
            return True
        else:
            #self.server.reconfig_job(job_name, config_xml)
            return False

    #创建视图
    def _create_view(self, project_name, jobs_list):
        jobs = self.server.get_all_jobs()
        modules_list = list()
        for module in jobs:
            if module['name'] in jobs_list:
                print(module['name'])
                modules_list.append(module['name'])

        name = '{project_name}'.format(project_name=project_name)
        env = Environment(loader=FileSystemLoader(searchpath='./templates'))
        template = env.get_template('jenkins-view-template.xml.j2')
        view_config = template.render(project_name=project_name,modules=modules_list)
        exist = self.server.get_view_name(name)
        if not exist:
            self.server.create_view(name, view_config)
        else:
            print("view已经存在")

    def run(self,project_id):
        project_info = get_settings_info(project_id)
        project_name = project_info['project_name']
        #project_name = "momtest"
        harbor_url = project_info['harbor_url']
        modules = project_info['modules']
        modules.append(project_info['register'])
        view_job_list = list()
        for module_info in modules:
            module_name, pro_port, dev_port, svn_address, module_type = module_info
            module_name = module_name.lower()
            job_name = "{project_name}-{module_name}".format(project_name=project_name,
                                                             module_name=module_name)

            config_xml = self._create_jenkins_config_xml(project_name, module_name, svn_address,
                                                             dev_port, pro_port, harbor_url)
            if module_type == "python":
                config_xml = self._create_jenkins_python_config_xml(project_name, module_name, svn_address,
                                                             dev_port, pro_port, harbor_url,python_image="python_{project_name}:3.6.1".format(project_name = project_name))
            if module_type == "front":
                config_xml = self._create_jenkins_staticresource_config_xml(project_name, module_name, svn_address)

            view_job_list.append(job_name)

            print("开始创建任务{job_name}".format(job_name = job_name))
            result = self._create_jenkins_job(job_name, config_xml)
            if result:
                print('创建成功!')
            else:
                print("job已经存在,请确认你的配置")

            #self.server.delete_job(job_name)

        print("开始创建jenkins视图")
        self._create_view("k8s_view", view_job_list)
        print("创建成功")
        #self.server.delete_view("k8s_view")

# jenkins = Jenkins()
# jenkins.run(11)



