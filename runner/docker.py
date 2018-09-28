import docker
import attr

@attr.s(frozen=True)

class DockerImageSetup:
    search_repositories: list = attr.ib()
    push_repository: str = attr.ib()
    commit: str = attr.ib()
    git_repo: str = attr.ib()
    dockerfile_folder: str = attr.ib()

    def build_docker_image(self):
        # Build a docker image from this commit
        client = docker.from_env()

        if self.dockerfile_folder:
            subfolder_suffix = ':' + self.dockerfile_folder
        else:
            subfolder_suffix = ''


        client.images.build(f'{self.git_repo}#{self.commit}{subfolder_suffix}'

            """acquire or build this docker tag"""
            """We enforce a convention of using docker tags that are simply the sha1 of the repository under test"""

            # Check locally and with list of registries to see if it already exists.

    def pull_or_build_docker_image(self):
        client = docker.from_env()

        image = client.images.pull("alpine", Tag='')

        """acquire or build this docker tag"""
        """We enforce a convention of using docker tags that are simply the sha1 of the repository under test"""

            # Check locally and with list of registries to see if it already exists.



    #docker build https://github.com/docker/rootfs.git

