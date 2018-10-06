import pytest
import docker
from runner import docker_runner


@pytest.fixture
def example_runner():
    return docker_runner.DockerImageSetup("imazen/imageflow_tool_testing", "ci/docker/hub/tool/Dockerfile",
                                   "https://github.com/imazen/imageflow.git",
                                   "4cbf721c36b461c22399f80252bae96004cd761d")


def test_pull(example_runner):
    assert example_runner.pull_image_if_missing()

def test_pull_nonexistent_repo():
    missing = docker_runner.DockerImageSetup("imazen/missing_repository", "",
                                          "https://github.com/imazen/imageflow.git",
                                          "4cbf721c36b461c22399f80252bae96004cd761d")
    assert not missing.pull_image_if_missing()

def test_pull_nonexistent_image():
    missing_image = docker_runner.DockerImageSetup("imazen/imageflow_tool_testing", "",
                                                   "https://github.com/imazen/imageflow.git",
                                                   "nonexistent")
    assert not missing_image.pull_image_if_missing()


def test_push(example_runner):
    assert example_runner.push_image()


def test_push_missing_repos():
    missing = docker_runner.DockerImageSetup("imazen/missing_repository", "",
                                          "https://github.com/imazen/imageflow.git",
                                          "4cbf721c36b461c22399f80252bae96004cd761d")
    assert not missing.push_image()


def test_image_present_local_missing_repo(example_runner):

    missing_repo = docker_runner.DockerImageSetup("imazen/missing_repository", "",
                                          "https://github.com/imazen/imageflow.git",
                                          "4cbf721c36b461c22399f80252bae96004cd761d")
    assert not missing_repo.image_present_local()

def test_image_present_local_missing_image(example_runner):
        missing_image = docker_runner.DockerImageSetup("imazen/imageflow_tool_testing", "",
                                                      "https://github.com/imazen/imageflow.git",
                                                      "nonexistent")
        assert not missing_image.image_present_local()


def test_build(example_runner):
    assert example_runner.build_image()


def test_build_missing_gitrepo():
    missing_git = docker_runner.DockerImageSetup("imazen/imageflow_tool_testing", "",
                                                   "https://github.com/imazen/nonexistent.git",
                                                   "4cbf721c36b461c22399f80252bae96004cd761d")
    with pytest.raises(docker.errors.APIError):
        missing_git.build_image()


def test_build_missing_gitcommit():
    missing_git = docker_runner.DockerImageSetup("imazen/imageflow_tool_testing", "",
                                                   "https://github.com/imazen/imageflow.git",
                                                   "4cbf721c36b461c22a99f80252bae96004cd761d")
    with pytest.raises(docker.errors.APIError):
        missing_git.build_image()


def test_ready(example_runner):
    assert example_runner.ready_image()


def test_ready_missing_gitcommit():
    missing_git = docker_runner.DockerImageSetup("imazen/imageflow_tool_testing", "",
                                                   "https://github.com/imazen/imageflow.git",
                                                   "4cbf721c36b461c22a99f80252bae96004cd761d")
    with pytest.raises(docker.errors.APIError):
        missing_git.ready_image()


