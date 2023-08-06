import os
import pathlib
import shutil

import jinja2

from tech.mlsql.plugin.tool.commands.compile_process import Spark311, Spark243, Spark330
from tech.mlsql.plugin.tool.shellutils import run_cmd


class PluginBuilder(object):
    def __init__(self,
                 mvn: str,
                 module_name: str,
                 spark: str
                 ):
        self.mvn = mvn
        self.module_name = module_name
        # spark311 / spark243
        self.spark = spark
        self.current_path = os.getcwd()

    def _builder(self):
        if self.spark == "spark311":
            builder = Spark311(self.current_path)
        elif self.spark == "spark243":
            builder = Spark243(self.current_path)
        elif self.spark == "spark330":
            builder = Spark330(self.current_path)
        else:
            raise Exception(f"spark {self.spark} is not support ")
        return builder

    def plugin_desc_convert(self, current_path: str):
        repo_path = os.path.join(current_path, '.repo')
        template_name = "desc.template.plugin"
        plugin_desc_path = os.path.join(repo_path, template_name)
        if not os.path.exists(plugin_desc_path):
            print(f"{plugin_desc_path} not exits,ignore")
            return

        print(f"load desc.template.plugin: {plugin_desc_path}")
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(repo_path))
        template = env.get_template(template_name)

        builder = self._builder()

        plugin_desc = template.render(spark_binary_version=builder.spark_binary_version,
                                      spark_version=builder.spark_version,
                                      scala_version=builder.scala_version,
                                      scala_binary_version=builder.scala_binary_version)

        target_plugin_desc_path = os.path.join(current_path, "desc.plugin")
        print(f"load desc.template.plugin: {os.path.join(plugin_desc_path, template_name)}")
        with open(target_plugin_desc_path, "w") as f:
            f.writelines(plugin_desc)

    def convert(self):
        self._convert(self.current_path)
        for file in os.listdir(self.current_path):
            if os.path.isdir(file) and not file.startswith(".") and os.path.exists(os.path.join(file, ".repo")):
                module_path = file
                self._convert(module_path)
                self.plugin_desc_convert(module_path)

    def _convert(self, current_path: str):
        if not os.path.exists(os.path.join(current_path, ".repo")):
            return
        if self.spark == "spark311":
            builder = Spark311(current_path)
        elif self.spark == "spark243":
            builder = Spark243(current_path)
        elif self.spark == "spark330":
            builder = Spark330(current_path)
        else:
            raise Exception(f"spark {self.spark} is not support ")
        builder.pom_convert()
        builder.source_convert()

    def build(self):
        self.convert()
        group = []
        with open("./{}/desc.plugin".format(self.module_name), "r") as f:
            config = {}
            for line in f.readlines():
                if line and line.strip():
                    clean_line = line.strip()
                    if clean_line == "__SPLITTER__":
                        group.append(config)
                        config = {}
                    else:
                        (k, v) = clean_line.split("=", 1)
                        config[k] = v
            group.append(config)
        jarPaths = []
        for config in group:
            plugin_name = config.get("moduleName") or self.module_name
            version = config["version"]
            scala_version = config["scala_version"]
            spark_version = "spark_version" in config and config["spark_version"]

            if not self.mvn:
                self.mvn = "mvn"

            spark_params = []
            if spark_version:
                spark_params = ["-Pspark-{}".format(spark_version)]
            command = [self.mvn, "-DskipTests", "clean",
                       "package", "-Pshade", ] + spark_params + ["-Pscala-{}".format(scala_version)] + ["-pl",
                                                                                                        self.module_name]
            run_cmd(command)
            jar_name = self.module_name
            if spark_version:
                jar_name = self.module_name + "-" + spark_version
            full_path = pathlib.Path().absolute()
            jar_final_name = "{}_{}-{}.jar".format(jar_name, scala_version, version)
            ab_file_path = os.path.join(full_path, self.module_name, "target",
                                        jar_final_name)
            build_path = os.path.join(full_path, self.module_name, "build")
            target_file = os.path.join(build_path, jar_final_name)
            if not os.path.exists(build_path):
                os.mkdir(build_path)
            shutil.copyfile(ab_file_path, target_file)
            jarPaths.append(target_file)

        print("====Build success!=====")
        i = 0
        for jarPath in jarPaths:
            print(" File location {}：\n {}".format(i, jarPath))
            i += 1
