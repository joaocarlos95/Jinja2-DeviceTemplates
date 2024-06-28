import os
import yaml
from jinja2 import Environment, FileSystemLoader


def get_j2_template(filename: str=None):
    '''
    Define the directory of Jinja2 templates and specify the base template (skeleton), or a
    specific template to be loaded.
    In case of base template, it will be extended by the child templates, specified by the 
    config_blocks variable passed in the constructor.
    '''

    # Set up the Jinja2 environment, specifying the directory where the base template is located
    base_dir = f"{os.path.dirname(os.path.abspath(__file__))}"
    env = Environment(
        loader=FileSystemLoader([base_dir, f"{base_dir}/templates"]), 
        trim_blocks=True, 
        lstrip_blocks=True)
    
    # Load the Jinja2 template specified by the filename parameter or use the base_config.j2 template
    filename = filename if filename else 'base_config.j2'
    j2_template = env.get_template(filename)
    return j2_template

def get_j2_data_from_file(filename: str=None):
    '''
    Get the data to be used in the jinja2 template, from a YAML file
    '''

    # Open the default config_data.yaml file and load the content to a variable
    with open(filename) as file:
        j2_data = yaml.safe_load(file)
    return j2_data

def render_j2_template(j2_template, j2_data):

    config = j2_template.render(j2_data)
    # Remove all leading spaces in the rendered configuration
    result = '\n'.join([line.lstrip() for line in config.split('\n')])
    return result

def main():

    j2_template = get_j2_template('extreme_snmp.j2')
    # j2_data = get_j2_data_from_file('extreme_exos_snmp.yaml')
    j2_data = {
        "snmpv3": {
            "groups": [
            {
                "name": "XMC_Group",
                "users": [
                {
                    "username": "snmpuser",
                    "auth_algorithm": "md5",
                    "auth_password": "snmpauthcred",
                    "priv_algorithm": "des",
                    "priv_password": "snmpprivcred"
                },
                {
                    "username": "ANAuser",
                    "auth_algorithm": "md5",
                    "auth_password": "ANApassword",
                    "priv_algorithm": "des",
                    "priv_password": "ANApassword"
                }
                ]
            }
            ],
            "traps": {
            "server_name": "XMC",
            "server_addr": "192.168.78.20",
            "port_number": 162,
            "vrf": None,
            "username": "snmpuser"
            }
        },
        "snmpv2c": {
            "groups": [
            {
                "name": "Cacti_Group",
                "users": [
                {
                    "username": "Cacti_User",
                    "community": "ANApassword"
                }
                ]
            }
            ]
        }
    }

    result = render_j2_template(j2_template, j2_data)
    print(result)
    return

if __name__ == "__main__":
    main()