# -*- coding: utf-8 -*-
import sys
import click

from tech.mlsql.plugin.tool.commands.builder import PluginBuilder
from tech.mlsql.plugin.tool.commands.compile_process import Spark311, Spark243, Spark330
from tech.mlsql.plugin.tool.http_manager import HttpManager


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
@click.option(
    "--mvn",
    required=False,
    type=str,
    help="mvn command")
@click.option(
    "--module_name",
    required=True,
    type=str,
    help="module name")
@click.option(
    "--spark",
    required=False,
    type=str,
    help="spark version")
def build(mvn: str, module_name: str, spark: str):
    builder = PluginBuilder(mvn, module_name, spark)
    builder.build()


@cli.command()
def scala211():
    builder = Spark243()
    builder.pom_convert()


@cli.command()
def scala212():
    builder = Spark311()
    builder.pom_convert()


@cli.command()
def spark311():
    builder = Spark311()
    builder.pom_convert()
    builder.source_convert()

@cli.command()
def spark330():
    builder = Spark330()
    builder.pom_convert()
    builder.source_convert()

@cli.command()
def spark243():
    builder = Spark243()
    builder.pom_convert()
    builder.source_convert()


@cli.command()
@click.option(
    "--jar_path",
    required=False,
    type=str,
    help="")
@click.option(
    "--module_name",
    required=False,
    type=str,
    help="")
@click.option(
    "--user",
    required=True,
    type=str,
    help="")
@click.option(
    "--password",
    required=True,
    type=str,
    help="")
def upload(jar_path, module_name, user, password):
    with open("./{}/desc.plugin".format(module_name), "r") as f:
        kvs = [line.strip().split("=", 1) for line in f.readlines() if "=" in line]
        config = dict([(kv[0], kv[1]) for kv in kvs])
    print(config)
    HttpManager.upload_plugin(store_path="http://store.mlsql.tech/run", file_path=jar_path,
                              data={"userName": user, "password": password,
                                    "pluginType": "MLSQL_PLUGIN",
                                    "pluginName": config["moduleName"], **config})


def main():
    return cli()


if __name__ == "__main__":
    main()
