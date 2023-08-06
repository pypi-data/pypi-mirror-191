#! /usr/bin/env python3

import click
import os
from .terraform import Terraform
import csv

def set_aws_credential (credential):
    if credential is not None:
        credential = os.path.abspath (credential)
        assert os.path.exists (credential), "credential not found"
        check_gitignore = False
    else:
        credential = os.path.join (os.getcwd (), ".protected/.awscredential.csv")
        check_gitignore = True

    if not os.path.exists (credential):
        return

    if check_gitignore:
        gitignore = os.path.join (os.getcwd (), ".gitignore")
        assert os.path.exists (gitignore), ".gitignore not found"
        with open (gitignore) as f:
            found = False
            for line in f:
                found = line.strip () == ".protected/"
                if found:
                    break
            assert found, ".gitignore must contain .protected/"

    with open (credential) as f:
        rd = csv.reader (f)
        id, key = -1, -1
        for idx, row in enumerate (rd):
            if idx == 0:
                for colnum, col in enumerate (row):
                    if col == 'Access key ID':
                        id = colnum
                    elif col == 'Secret access key':
                        key = colnum
            elif idx == 1:
                assert id > -1 and key > -1
                os.environ ["AWS_ACCESS_KEY_ID"], os.environ ["AWS_SECRET_ACCESS_KEY"] = row [id], row [key]
                break


# commands --------------------------------------------------
@click.group()
@click.option ('-c', '--credential', default = None)
@click.option ('-f', '--file', default = None)
@click.option ('-s', '--silent', is_flag = True)
@click.pass_context
def cli (context, file, credential, silent):
    set_aws_credential (credential)

    if file is None:
        file = os.path.join (os.getcwd (), "docker-compose.yml")
        if not os.path.isfile (os.path.abspath (file)):
            file = os.path.join (os.getcwd (), "compose.ecs.yml")
    file = os.path.abspath (file)
    assert os.path.isfile (file), f"{file} not found"

    with open (file) as f:
        context.obj ["cli"] = Terraform (f.read (), path = file, silent = silent)


CLUSTER_SUBCOMMANDS = ("create", "destroy", "update", "show", "plan")
@cli.command ()
@click.argument ('subcommand')
@click.option ('-y', '--yes', is_flag = True)
@click.pass_context
def cluster (context, subcommand, yes):
    """
    SUBCOMMAND: create | destroy | update | show | plan
    """
    assert subcommand in CLUSTER_SUBCOMMANDS
    cli = context.obj ["cli"]
    out_tf = cli.generate_cluster_declares ()
    if subcommand == "show":
        print (out_tf)
        return
    if subcommand in ("create", "update", "plan"):
        return cli.create_cluster (subcommand == "plan")

    if not yes:
        cluter_name = cli.d ["x-ecs-cluster"]['name']
        ans = input (f"You are going to destroy cluster, type `{cluter_name}` if you are sure: ")
        if ans != cluter_name:
            print ('canceled')
            return
    cli.remove_cluster ()


SERVICE_SUBCOMMANDS = ("up", "down", "show", "plan")
@cli.command ()
@click.argument ('subcommand')
@click.argument ('stage', envvar = 'SERVICE_STAGE', default = "qa")
@click.argument ('tag', envvar = 'CI_COMMIT_SHA', default = "latest")
@click.option ('-y', '--yes', is_flag = True)
@click.option ('-t', '--latest', is_flag = True)
@click.pass_context
def service (context, subcommand, stage, tag, latest, yes):
    """
    SUBCOMMAND: up | down | show | plan
    """
    if latest:
        tag = "latest"
    assert subcommand in SERVICE_SUBCOMMANDS
    cli = context.obj ["cli"]
    out_tfs = cli.generate_service_declares (stage, tag [:8])
    if subcommand == "show":
        for k, v in out_tfs.items ():
            print (k)
            print ('───────────────────────────────────────────────────────')
            print (v)
        return

    if subcommand in ("up", "plan"):
        return cli.deploy_service (stage, subcommand == "plan")
    if not yes:
        service_name = cli.d ["x-ecs-service"]['name']
        ans = input (f"You are going to shutdown service, type `{service_name}` if you are sure: ")
        if ans != service_name:
            print ('canceled')
            return
    return cli.remove_service (stage)


def main ():
    cli (obj = {})

if __name__ == "__main__":
    main ()
