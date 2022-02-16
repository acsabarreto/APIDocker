import argparse
import yaml


def generate_conf(deploy_file_src, deploy_file_dst, cpu, memory):
    with open(deploy_file_src, 'r') as file:
        yaml_file = yaml.safe_load(file)

    containers = yaml_file['spec']['template']['spec']['containers']
    resources = containers[0]['resources']
    resources['limits']['memory'] = memory
    resources['limits']['cpu'] = cpu
    resources['requests']['memory'] = memory
    resources['requests']['cpu'] = cpu

    with open(deploy_file_dst, 'w') as file:
        yaml.dump(yaml_file, file)


def rename_dst_file(deploy_file_dst, index):

    file = deploy_file_dst.split('/')[-1]
    newName = file.split('.')[0]
    newName = newName + str(index) + '.yaml'
    deploy_file_dst = deploy_file_dst.replace(file, newName)

    return deploy_file_dst


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--deployFileSrc', help='Deployment Source File',
                        type=str, required=True)
    parser.add_argument('--deployFileDst', help='Deployment Destination File',
                        type=str, required=True)
    parser.add_argument('--configsFile', help='Configs File',
                        type=str, required=True)

    args = parser.parse_args()

    with open(args.configsFile, 'r') as file:
        configs = yaml.safe_load(file)

    deployFileSrc = args.deployFileSrc

    index = 1
    for config in configs['configs']:
        cpu = config['resources']['cpu']
        memory = config['resources']['memory']
        deployFileDst = rename_dst_file(deploy_file_dst=args.deployFileDst,
                                        index=index)
        generate_conf(deployFileSrc, deployFileDst, cpu, memory)
        index += 1



