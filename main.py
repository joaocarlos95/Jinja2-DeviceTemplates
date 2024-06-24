import yaml
from jinja2 import Environment, FileSystemLoader


def get_j2_template(filename: str=None):
    '''
    Define the directory of jinja2 templates and specify the base template (skeleton) to be loaded
    The base_config.j2 template will then be extended by the child templates, specified by the 
    config_blocks variable passed in the constructor
    '''

    # Load the base template and assign it to a variable for further usage
    env = Environment(
        loader=FileSystemLoader(['.', './templates']), 
        trim_blocks=True, 
        lstrip_blocks=True)
    
    filename = filename if filename else 'base_config.j2'
    j2_base_template = env.get_template(filename)
    return j2_base_template

def get_j2_data():
    '''
    Get the data to be used in the jinja2 template, from a YAML file
    '''

    # Open the default config_data.yaml file and load the content to a variable
    with open(f"{dir}/inputfiles/config_data.yaml") as file:
        j2_data = yaml.safe_load(file)

def main():

    environment = Environment(loader=FileSystemLoader('path/to/templates'))
    template = environment.get_template('template.html')

    # Define the data to be passed to the template
    data = {
        'title': 'My Page Title',
        'heading': 'Welcome to My Page',
        'description': 'This is a description of my page.',
        'items': ['Item 1', 'Item 2', 'Item 3']
    }

    # Render the template with the data
    output = template.render(data)

    # Print the rendered template (or write it to a file)
    print(output)

if __name__ == "__main__":
    main()