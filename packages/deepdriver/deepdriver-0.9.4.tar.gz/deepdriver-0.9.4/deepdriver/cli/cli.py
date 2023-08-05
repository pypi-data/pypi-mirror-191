import argparse
import os

from click import UsageError

import deepdriver
import click
import re
import configparser
import pipes
import pickle

from deepdriver.cli import cli_func
from deepdriver.cli.cli_ctx import Config, CommandGroup

pass_config = click.make_pass_decorator(Config, ensure=True)


def read_config(ctx, param, value):
    """Callback that is used whenever --config is passed.  We use this to
    always load the correct config.  This means that the config is loaded
    even if the group itself never executes so our aliases stay always
    available.
    """
    cfg = ctx.ensure_object(Config)
    if value is None:
        value = os.path.join(os.path.dirname(__file__), "aliases.ini")
    cfg.read_config(value)
    return value


@click.command(cls=CommandGroup)
@click.pass_context
def cli(ctx):
    ctx.obj = Config()


@click.command('setting', short_help='Initialize the Deepdriver Host Setting.')
@pass_config
# @click.option('--http_host', cls=OptionDefaultFromContext, default_section="DEFAULT", default_key="HTTP_HOST", default_value="15.164.104.132:9011", required=True, callback=test, help='REST API Server URI',
#               prompt="Please enter HTTP API Server URI", )
@click.option('--http_host', callback=cli_func.test, help='REST API Server URI', required=True)
@click.option('--grpc_host', callback=cli_func.test, help='GRPC Server URI', required=True)
def setting(config, http_host, grpc_host):
    """ Save HTTP API Server URI and GRPC Server URI To Config fily """

    click.echo('Initializing the Deepdriver Host Setting')

    if config.http_host and config.grpc_host:
        click.echo(click.style('Deepdriver Setting file already exists.', fg='red'))
        if click.confirm('Do you want to overwrite?', abort=False):
            config.http_host = http_host
            config.grpc_host = grpc_host
            config.save()


@click.command('login', short_help='Login to The Deepdriver')
@click.option('--key', help='Login Key', required=True)
@pass_config
def login(config, key):
    # deepdriver setting 체크
    if not cli_func.check_is_setting(config):
        return

    if config.key:  # key가 이미 존재할 경우 overwrite 여부
        click.echo(click.style('Deepdriver login key already exists.', fg='red'))
        if not click.confirm('Do you want to overwrite?', abort=False):
            return

    if config.token:  # token이 이미 존재할 경우 overwrite 여부
        click.echo(click.style('Deepdriver login token already exists.', fg='red'))
        if not click.confirm('Do you want to overwrite?', abort=False):
            return

    try:
        # deepdriver setting host
        cli_func.api_setting(config)

        # login 처리
        login_result, jwt_token = deepdriver.login(key=key)
    except Exception as e:
        click.echo(click.style(f"Login Failed : {str(e)}", fg='red'))
        return

    if login_result:
        # token을 파일에 저장
        click.echo(click.style("Login Success", fg='green'))
        config.key = key
        config.token = jwt_token
        config.save()


@click.command('init', short_help='Initialize the Deepdriver Experiment')
@click.option('--exp_name', help='Experiment Name', required=True)
@click.option('--team_name', help='Team Name', default="", required=False)
@pass_config
def init(config, exp_name, team_name):
    # deepdriver setting 체크
    if not cli_func.check_is_setting(config):
        return

    # deepdriver login 체크
    if not cli_func.check_is_login(config):
        return

    # if exp_name is None:
    #     exp_name = click.prompt(
    #         f"Please enter Experiment Name",
    #         show_default=False,
    #         value_proc=check_exp_name
    #     )
    # if team_name is None:
    #     team_name = click.prompt(
    #         f"Please enter Team Name",
    #         default="",
    #         show_default=False,
    #     )

    cli_func.api_setting(config)
    cli_func.api_login(config)

    run = deepdriver.init(exp_name=exp_name, team_name=team_name)

    cli_func.run_dump(path_dir=config.config_base_dir, run=run)


@click.command('artifact', short_help='Upload or Download the Deepdriver Artifact')
@click.argument('command', type=click.Choice(['upload', 'download'], case_sensitive=False))
@click.option('--type', help='Type of artifact', prompt="Select type f Artifact",
              type=click.Choice(['model', 'dataset', 'code']), required=True)
@click.option('--name', help='Name of artifact', prompt="Input the name of Artifact", required=True)
@click.option('--tag', help='Tag of artifact', required=False)
@click.argument('path', type=click.Path(exists=True, file_okay=False, resolve_path=True), required=True)
@pass_config
def artifact(config, command, type, name, tag, path):
    if command == 'upload':  # upload artifact
        cli_func.api_setting(config)
        cli_func.api_login(config)

        run = cli_func.run_load(path_dir=config.config_base_dir)

        from deepdriver.sdk.data_types.run import set_run, Run, get_run
        set_run(run)

        arti = deepdriver.get_artifact(**{"type": type, "name": name, "tag": tag})
        print(f"artfact info : {arti.__dict__}")
        arti.add(path)
        deepdriver.upload_artifact(arti)


    elif command == 'download':
        cli_func.api_setting(config)
        cli_func.api_login(config)

        run = cli_func.run_load(path_dir=config.config_base_dir)

        from deepdriver.sdk.data_types.run import set_run, Run, get_run
        set_run(run)
        arti = deepdriver.get_artifact(**{"type": type, "name": name, "tag": tag})
        arti.download(path)


cli.add_command(setting)
cli.add_command(login)
cli.add_command(init)
cli.add_command(artifact)

if __name__ == "__main__":
    cli()
