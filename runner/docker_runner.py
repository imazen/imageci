import docker
import attr
import tarfile
import time
from io import BytesIO
from runner.docker_setup import DockerImageSetup


@attr.s(frozen=True)
class DockerExecConfig:
    """Where should the tarstream be decompressed?"""
    env_vars = attr.ib()  # Environment variables

    input_path: str = attr.ib()
    input_tarstream: BytesIO = attr.ib()

    command: str = attr.ib()
    output_path: str = attr.ib()  # What folder contains the output files?
    results_consumer = attr.ib()  # Consumes DockerExecResults, produces TestResult

    @staticmethod
    def tar_job(job_json: str, input_files_bytes: list):
        stream = BytesIO()
        tar = tarfile.TarFile(fileobj=stream, mode='w')

        json_data = job_json.encode('utf8')
        json_meta = tarfile.TarInfo(name='job.json')
        json_meta.size = len(json_data)
        json_meta.mtime = time.time()
        # json_meta.mode = 0600
        tar.addfile(json_meta, BytesIO(json_data))

        for ix, input_bytes in enumerate(input_files_bytes):
            input_meta = tarfile.TarInfo(name=str(ix))
            input_meta.size = len(input_bytes)
            input_meta.mtime = time.time()
            tar.addfile(input_meta, BytesIO(input_bytes))

        tar.close()

        stream.seek(0)
        return stream


@attr.s(frozen=True)
class DockerExecResults:
    message: str = attr.ib()
    setup_failed: bool = attr.ib()
    exit_code: int = attr.ib()
    output: bytes = attr.ib()
    files_tar: BytesIO = attr.ib()
    docker_logs: bytes = attr.ib()

    def success(self):
        return not self.setup_failed and (self.exit_code == 0)

    def logs(self):
        return self.message + "\n" + str(self.output) + "\n" + str(self.docker_logs)

    def test_result_default(self):
        return TestResult(self.success(), self.logs())


@attr.s(frozen=True)
class TestResult:
    success: bool = attr.ib()
    debug: str = attr.ib()

# If you get OCI runtime exec failed: exec failed: container_linux.go:348: starting container process caused "process_linux.go:86: executing setns process caused exit status 21
# Then you need to create the container with stdin_open=True

# Note that the home directory ~ will not resolve - you are running commands directly, not under bash expansion

@attr.s(frozen=True)
class ContainerTool:
    api = attr.ib()
    id: str = attr.ib()

    def mkdir(self, path: str, debug: bool = True):
        return self.run(f"/bin/bash -c 'mkdir {path} && ls ~/'", debug)

    def run(self, commands, debug: bool = True):
        exec = self.api.exec_create(self.id, commands)
        if debug:
            print(self.api.exec_inspect(exec['Id']))
        output = self.api.exec_start(exec_id=exec['Id'])
        if debug:
            print(output)

        return self.api.exec_inspect(exec)['ExitCode'], output

@attr.s(frozen=True)
class DockerRunner:
    setup: DockerImageSetup = attr.ib()
    config: DockerExecConfig = attr.ib()

    def exec_within_container(self, api, container_id):

        tool = ContainerTool(api, container_id)

        exit_code, output = tool.mkdir(self.config.input_path)
        if not exit_code == 0:
            return DockerExecResults(f"Failed to create input directory {self.config.input_path}", True, exit_code, output, None, api.logs(container_id))

        exit_code, output = tool.mkdir(self.config.output_path)
        if not exit_code == 0:
            return DockerExecResults(f"Failed to create output directory {self.config.output_path}", True, exit_code,
                                     output, None, api.logs(container_id))

        if not api.put_archive(container_id,
                path=self.config.input_path,
                data=self.config.input_tarstream
        ):
            return DockerExecResults("Failed to inject input files", True, exit_code, output, None, api.logs(container_id))

        exit_code, output = tool.run(f"ls {self.config.input_path}")

        if not exit_code == 0:
            return DockerExecResults(f"Failed to list {self.config.input_path}", True, exit_code, output, None, api.logs(container_id))

        exit_code, output = tool.run(self.config.command)
        output_tar = api.get_archive(container=container_id, path=self.config.output_path)


        # exit_code, output = tool.run(f"ls {self.config.output_path}")
        # if not exit_code == 0:
        #     return DockerExecResults(f"Failed to list {self.config.output_path}", True, exit_code, output, None,
        #                              api.logs(container_id))
        #

        return DockerExecResults("", False, exit_code, output, output_tar, api.logs(container_id))


    def run(self):
        client = docker.from_env()
        api = client.api
        print(f"Creating container from {self.setup.tagged_image}")
        container = api.create_container(self.setup.tagged_image, 'cat', detach=True, stdin_open=True)
        container_id = container['Id']
        try:
            api.start(container_id)
            try:
                return self.config.results_consumer(self.exec_within_container(api, container_id))
            # todo: catch
            finally:
                api.stop(container_id, force=True)
        finally:
            api.remove_container(container_id, force=True, v=True)


class ImageflowRunner:
    def config(self):
        return DockerExecConfig({}, "/home/imageflow/input/", DockerExecConfig.tar_job("""{
  "builder_config": null,
  "io": [
    {
      "io_id": 0,
      "direction": "in",
      "io": "placeholder"
    },
    {
      "io_id": 1,
      "direction": "out",
      "io": "placeholder"
    },
    {
      "io_id": 2,
      "direction": "out",
      "io": "placeholder"
    },
    {
      "io_id": 3,
      "direction": "out",
      "io": "placeholder"
    },
    {
      "io_id": 4,
      "direction": "out",
      "io": "placeholder"
    }
  ],
  "framewise": {
    "graph": {
      "nodes": {
        "6": {
          "encode": {
            "io_id": 2,
            "preset": {
              "libjpegturbo": {
                "quality": 90,
                "progressive": null,
                "optimize_huffman_coding": null
              }
            }
          }
        },
        "2": {
          "constrain": {
            "within": {
              "w": 1200,
              "h": null,
              "hints": null
            }
          }
        },
        "7": {
          "encode": {
            "io_id": 3,
            "preset": {
              "libjpegturbo": {
                "quality": 90,
                "progressive": null,
                "optimize_huffman_coding": null
              }
            }
          }
        },
        "5": {
          "encode": {
            "io_id": 1,
            "preset": {
              "libjpegturbo": {
                "quality": 90,
                "progressive": null,
                "optimize_huffman_coding": null
              }
            }
          }
        },
        "8": {
          "encode": {
            "io_id": 4,
            "preset": {
              "libjpegturbo": {
                "quality": 90,
                "progressive": null,
                "optimize_huffman_coding": null
              }
            }
          }
        },
        "1": {
          "constrain": {
            "within": {
              "w": 1600,
              "h": null,
              "hints": null
            }
          }
        },
        "3": {
          "constrain": {
            "within": {
              "w": 800,
              "h": null,
              "hints": null
            }
          }
        },
        "4": {
          "constrain": {
            "within": {
              "w": 400,
              "h": null,
              "hints": null
            }
          }
        },
        "0": {
          "decode": {
            "io_id": 0,
            "commands": null
          }
        }
      },
      "edges": [
        {
          "from": 4,
          "to": 8,
          "kind": "input"
        },
        {
          "from": 2,
          "to": 4,
          "kind": "input"
        },
        {
          "from": 1,
          "to": 2,
          "kind": "input"
        },
        {
          "from": 0,
          "to": 1,
          "kind": "input"
        },
        {
          "from": 3,
          "to": 7,
          "kind": "input"
        },
        {
          "from": 1,
          "to": 3,
          "kind": "input"
        },
        {
          "from": 2,
          "to": 6,
          "kind": "input"
        },
        {
          "from": 1,
          "to": 5,
          "kind": "input"
        }
      ]
    }
  }
}""", []),"./imageflow_tool v0.1/build --json /home/imageflow/input/job.json --in http://s3-us-west-2.amazonaws.com/imageflow-resources/test_inputs/waterhouse.jpg --out 1 /home/imageflow/output/waterhouse_w1600.jpg 2 /home/imageflow/output/waterhouse_w1200.jpg 3 /home/imageflow/output/waterhouse_w800.jpg 4 /home/imageflow/output/waterhouse_w400.jpg --response /home/imageflow/output/operation_result.json",
     "/home/imageflow/output/", results_consumer=ImageflowRunner.process_results)

    @staticmethod
    def process_results(results: DockerExecResults):
        return results.test_result_default()
