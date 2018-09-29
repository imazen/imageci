import docker
import attr


@attr.s(frozen=True)
class DockerImageSetup:
    docker_repo: str = attr.ib()
    dockerfile: str = attr.ib("Dockerfile")
    git_repo: str = attr.ib(None) #requires .git suffix
    commit: str = attr.ib(None)
    override_docker_tag: str = attr.ib(None)

    @property
    def docker_tag(self):
        """We try for a convention of using docker tags that are simply the sha1 of the repository under test"""
        return self.override_docker_tag or self.commit

    @property
    def tagged_image(self):
        return f'{self.docker_repo}:{self.docker_tag}'


    def build_image(self):
        if not self.git_repo or not self.commit:
            return False
        # Build a docker image from this commit and tag it with the commit
        client = docker.from_env()

        build_result = client.images.build(path=f'{self.git_repo}#{self.commit}',
                                           tag=f'{self.docker_repo}:{self.docker_tag}',
                                           dockerfile=self.dockerfile,
                                           buildargs={'SOURCE_COMMIT': self.commit})

        return build_result

    def push_image(self):
        client = docker.from_env()

        push_result = client.images.push(self.docker_repo,tag=self.docker_tag)
        #print(push_result)
        return not "errorDetail" in push_result

    def pull_image_if_missing(self):
        client = docker.from_env()
        if self.image_present_local():
            return True
        try:
            client.images.pull(self.docker_repo, tag=self.docker_tag)
        except docker.errors.NotFound:
            return False
        return True


    def image_present_local(self):
        client = docker.from_env()
        try:
            if client.images.get(self.tagged_image):
                return True
            else:
                return False
        except docker.errors.ImageNotFound:
            return False

    def ready_image(self):
        if self.pull_image_if_missing():
            return True
        else:
            return self.build_image()


@attr.s(frozen=True)
class DockerRunner:
    setup: DockerImageSetup = attr.ib()

    def run(self):
        client = docker.from_env()
        container = client.containers.create(self.setup.tagged_image)
        #copy files in
        #invoke
        #copy files out


