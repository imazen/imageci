import pytest
import docker
from runner.docker_runner import DockerRunner, DockerExecConfig, DockerExecResults, ImageflowRunner
from runner.docker_setup import DockerImageSetup



def test_run_imageflow():
    imageflow = DockerImageSetup("imazen/imageflow_tool_imageci", "docker/imageflow_tool_imageci/Dockerfile",
                                   "https://github.com/imazen/imageflow.git",
                                   "9c42df788fc8163357259a2a81142619005e9995")

    print("Getting docker image ready")
    assert imageflow.ready_image()

    exec_config = ImageflowRunner().config()

    test_result = DockerRunner(imageflow, exec_config).run()
    assert test_result.success, test_result.debug



def test_execute_command():
    client = docker.from_env().api
    client.pull('busybox:latest')
    container = client.create_container('busybox:latest', 'cat', stdin_open=True)
    id = container['Id']
    client.start(id)

    res = client.exec_create(id, ['echo', 'hello'])
    assert 'Id' in res

    exec_log = client.exec_start(res)
    assert exec_log == b'hello\n'

    res = client.exec_create(id, ['/bin/false'])
    exec_log = client.exec_start(res)
    assert exec_log == b''
    assert client.exec_inspect(res)['ExitCode'] == 1

    res = client.exec_create(id, ['/bin/sh', '-c', '(>&2 echo "error")'])

    exec_log = client.exec_start(res)
    assert exec_log == b'error\n'
    assert client.exec_inspect(res)['ExitCode'] == 0