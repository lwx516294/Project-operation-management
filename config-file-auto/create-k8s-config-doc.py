from jinja2 import Environment, FileSystemLoader
import os
from .config.settings import *


class CreateKubernetesConfigFile:
    def __init__(self, project_name, module_name, stage, register_module_name, harbor_url, register_port, port=None,
                 java_mem_requests=128, java_mem_limits=256, mem_requests=128, mem_limits=512, is_register=False):
        self.is_register = is_register

        self.deployment_variables = {
            'project_name': project_name,
            'module_name': module_name,
            'stage': stage,
            'register_module_name': register_module_name,
            'harbor_url': harbor_url,
            'register_port': register_port,
        }

        self.resource_limit = {
            'java_mem_requests': java_mem_requests,
            'java_mem_limits': java_mem_limits,
            'mem_requests': mem_requests,
            'mem_limits': mem_limits,
        }

        self.service_variables = {
            'project_name': project_name,
            'module_name': module_name,
            'stage': stage,
            'port': port
        }

        self.deployment_register_variables = {
            'project_name': project_name,
            'module_name': module_name,
            'stage': stage,
            'register_module_name': register_module_name,
            'harbor_url': harbor_url,
        }

        self.service_register_variables = {
            'project_name': project_name,
            'module_name': module_name,
            'stage': stage,
            'port': register_port
        }

    def _create_k8s_deployment_config_doc(self):
        if not self.is_register:
            deployment_template = 'k8s-deployment-template.yaml.j2'
            variables = self.deployment_variables

        else:
            deployment_template = 'k8s-register-deployment-template.yaml.j2'
            variables = self.deployment_register_variables

        env = Environment(loader=FileSystemLoader(searchpath='./templates'))
        template = env.get_template(deployment_template)

        config_doc = template.render(**variables, **self.resource_limit)
        file_name = "{project_name}-{module_name}-deployment" \
                    "-{stage}.yaml".format(project_name=self.deployment_variables['project_name'],
                                           module_name=self.deployment_variables['module_name'],
                                           stage=self.deployment_variables['stage'])

        dir_name = "{project_name}/{stage}/" \
                   "{module_name}".format(project_name=self.deployment_variables['project_name'],
                                          stage=self.deployment_variables['stage'],
                                          module_name=self.deployment_variables['module_name'])

        self._write_config_file(dir_name, file_name, config_doc)

    def _create_k8s_service_config_doc(self):
        if not self.is_register:
            variables = self.service_variables
        else:
            variables = self.service_register_variables
        env = Environment(loader=FileSystemLoader(searchpath='./templates'))
        template = env.get_template('k8s-service-template.yaml.j2')
        config_doc = template.render(**variables)

        file_name = "{project_name}-{module_name}-service" \
                    "-{stage}.yaml".format(project_name=self.deployment_variables['project_name'],
                                           module_name=self.deployment_variables['module_name'],
                                           stage=self.deployment_variables['stage'])

        dir_name = "{project_name}/{stage}/" \
                   "{module_name}".format(project_name=self.deployment_variables['project_name'],
                                          stage=self.deployment_variables['stage'],
                                          module_name=self.deployment_variables['module_name'])
        self._write_config_file(dir_name, file_name, config_doc)

    def create_k8s_config_doc(self):
        self._create_k8s_deployment_config_doc()
        self._create_k8s_service_config_doc()

    def _write_config_file(self, dir_name, file_name, doc):
        self._create_dir(dir_name)
        file = "{dir_name}/{file_name}".format(dir_name=dir_name, file_name=file_name)
        with open(file, 'w') as conf_file:
            conf_file.write(doc)

    @staticmethod
    def _create_dir(dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)


def create_jenkins_config_file(project_name, module_name, svn_address, dev_port, pro_port, ):
    env = Environment(loader=FileSystemLoader(searchpath='./templates'))
    template = env.get_template('jenkins-template.j2')
    config_doc = template.render(project_name=project_name, module_name=module_name, svn_address=svn_address,
                                 dev_port=dev_port, pro_port=pro_port)

    dir_name = "{project_name}/jenkins/".format(project_name=project_name,)
    file_name = "{project_name}-{module_name}.jenkins".format(project_name=project_name, module_name=module_name)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    file = "{dir_name}/{file_name}".format(dir_name=dir_name, file_name=file_name)
    with open(file, 'w') as conf_file:
        conf_file.write(config_doc)


def run():
    project_name = project_info['project_name']
    stages = project_info['stages']
    modules = project_info['modules']
    harbor_url = project_info['harbor_url']
    for stage in stages:
        register_info = project_info['register']
        register_module_name, register_pro_port, register_dev_port, svn_address, module_type = register_info
        register_module_name = register_module_name.lower()
        if stage == 'dev':
            register_port = register_dev_port
        else:
            register_port = register_pro_port

        # 创建注册中心模块信息
        config = CreateKubernetesConfigFile(project_name, register_module_name, stage,
                                            register_module_name, harbor_url, register_port, is_register=True)
        config.create_k8s_config_doc()

        # 创建模块信息
        for module_info in modules:
            module_name, pro_port, dev_port, svn_address, module_type = module_info
            module_name = module_name.lower()
            if stage == 'dev':
                port = dev_port
            else:
                port = pro_port
            if module_type == 'java':
                config = CreateKubernetesConfigFile(project_name, module_name, stage,
                                                    register_module_name, harbor_url, register_port, port)
                config.create_k8s_config_doc()


if __name__ == '__main__':
    run()




