'''
This is the CLI for the mlpath package. Includes commands to create a new project
'''
# pylint: skip-file

import zipfile
import click
import os
import pkg_resources

# if a name is provided make the directory with that name
@click.command()
@click.option('--name', default='Project', help='The name of the project')
@click.option('--full', default=False, is_flag=True, help='A simpler project directory will be created if this flag is set')

def main(name, full):
    zip_name = 'simple-project' if not full else 'project'
    try:
        zip_path = pkg_resources.resource_filename(__name__, f"/{zip_name}.zip")
        with zipfile.ZipFile(zip_path,"r") as zip_ref:
            zip_ref.extractall(name)
        click.echo('Project created successfully')
        
    except Exception as e:
        click.echo('Project creation failed')
        click.echo(e)

