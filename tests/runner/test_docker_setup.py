import pytest
import docker
from runner.docker_setup import DockerImageSetup


@pytest.fixture
def example_runner():
    return DockerImageSetup("imazen/imageflow_tool_imageci", "docker/imageflow_tool_imageci/Dockerfile",
                                   "https://github.com/imazen/imageflow.git",
                                   "9c42df788fc8163357259a2a81142619005e9995")


def test_pull(example_runner):
    assert example_runner.pull_image_if_missing()

def test_pull_nonexistent_repo():
    missing = DockerImageSetup("imazen/missing_repository", "",
                                          "https://github.com/imazen/imageflow.git",
                                          "4cbf721c36b461c22399f80252bae96004cd761d")
    assert not missing.pull_image_if_missing()

def test_pull_nonexistent_image():
    missing_image = DockerImageSetup("imazen/imageflow_tool_imageci", "",
                                                   "https://github.com/imazen/imageflow.git",
                                                   "nonexistent")
    assert not missing_image.pull_image_if_missing()


def test_push(example_runner):
    assert example_runner.push_image()


def test_push_missing_repos():
    missing = DockerImageSetup("imazen/missing_repository", "",
                                          "https://github.com/imazen/imageflow.git",
                                          "4cbf721c36b461c22399f80252bae96004cd761d")
    assert not missing.push_image()


def test_image_present_local_missing_repo(example_runner):

    missing_repo = DockerImageSetup("imazen/missing_repository", "",
                                          "https://github.com/imazen/imageflow.git",
                                          "4cbf721c36b461c22399f80252bae96004cd761d")
    assert not missing_repo.image_present_local()

def test_image_present_local_missing_image(example_runner):
        missing_image = DockerImageSetup("imazen/imageflow_tool_imageci", "",
                                                      "https://github.com/imazen/imageflow.git",
                                                      "nonexistent")
        assert not missing_image.image_present_local()


@pytest.mark.skip(reason="Takes a couple minutes, since it has to compile Imageflow every time")
def test_build(example_runner):
    assert example_runner.build_image()


def test_build_missing_gitrepo():
    missing_git = DockerImageSetup("imazen/imageflow_tool_imageci", "",
                                                   "https://github.com/imazen/nonexistent.git",
                                                   "4cbf721c36b461c22399f80252bae96004cd761d")
    with pytest.raises(docker.errors.APIError):
        missing_git.build_image()


def test_build_missing_gitcommit():
    missing_git = DockerImageSetup("imazen/imageflow_tool_imageci", "",
                                                   "https://github.com/imazen/imageflow.git",
                                                   "4cbf721c36b461c22a99f80252bae96004cd761d")
    with pytest.raises(docker.errors.APIError):
        missing_git.build_image()


def test_ready(example_runner):
    assert example_runner.ready_image()


def test_ready_missing_gitcommit():
    missing_git = DockerImageSetup("imazen/imageflow_tool_imageci", "",
                                                   "https://github.com/imazen/imageflow.git",
                                                   "4cbf721c36b461c22a99f80252bae96004cd761d")
    with pytest.raises(docker.errors.APIError):
        missing_git.ready_image()


