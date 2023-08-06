import logging
import os
from uuid import uuid4

import click
from packaging.version import InvalidVersion
from packaging.version import parse as version_parser

from fourdigits_cli.settings import DEFAULT_CONFIG
from fourdigits_cli.utils.docker import Docker, DockerException
from fourdigits_cli.utils.git import Git

logger = logging.getLogger(__name__)

group = click.Group(help="Docker helper command for auto building and pushing")


@click.group()
@click.option(
    "--registry-domain",
    help="Defaults to docker.io, env override DOCKER_REGISTRY_DOMAIN",
)
@click.option("--registry-user", help="env override DOCKER_REGISTRY_USER")
@click.option("--registry-password", help="env override DOCKER_REGISTRY_PASSWORD")
@click.option(
    "--image-user",
    help=f"Defaults to settings ({DEFAULT_CONFIG.docker_image_user}), env override DOCKER_IMAGE_USER",  # noqa: E501
)
@click.pass_context
def group(ctx, **options):
    ctx.obj = Docker(
        registry_user=options["registry_user"]
        or os.environ.get("DOCKER_REGISTRY_USER"),
        registry_password=options["registry_password"]
        or os.environ.get("DOCKER_REGISTRY_PASSWORD"),
        registry=options["registry_domain"]
        or os.environ.get("DOCKER_REGISTRY_DOMAIN", "docker.io"),
        image_user=options["image_user"]
        or os.environ.get("DOCKER_IMAGE_USER", DEFAULT_CONFIG.docker_image_user),
    )


@group.command(help="Build given environment")
@click.argument("environment")
@click.option(
    "--version",
    help="Version to build. If no version is supplied, it will try to get the current git tag",  # noqa: E501
)
@click.option("--push", is_flag=True, show_default=True, default=False)
@click.option("--target")
@click.option("--file", default="Dockerfile", show_default=True)
@click.option("--context", default=".", show_default=True)
@click.pass_obj
def build(docker: Docker, environment, **options):
    if environment not in DEFAULT_CONFIG.environments:
        raise click.UsageError("Environment doesn't exists in the pyproject.toml")

    version = validate_and_get_version(environment, version=options.get("version"))

    # Download the latest image to increase build process
    latest_image = docker.get_image_name(
        repo=DEFAULT_CONFIG.docker_repo, tag=environment
    )
    try:
        docker.pull(latest_image)
    except DockerException:
        latest_image = None

    # Docker build, tag and push image
    build_image_name = uuid4().hex
    try:
        docker.build(
            build_image_name,
            file=options.get("file"),
            context=options.get("context"),
            target=options.get("target"),
            build_tag=str(version),
            cache_from=latest_image,
        )
        for tag in [environment, str(version)]:
            docker.image_tag(
                build_image_name,
                docker.get_image_name(
                    repo=DEFAULT_CONFIG.docker_repo,
                    tag=tag,
                ),
            )
            if options.get("push"):
                docker.push(
                    docker.get_image_name(
                        repo=DEFAULT_CONFIG.docker_repo,
                        tag=tag,
                    )
                )
    except DockerException as e:
        raise click.UsageError(e)


def validate_and_get_version(environment, version=None):
    if version:
        if validate_version(environment, version):
            return version
        else:
            raise click.UsageError(
                f"Invalid version format ({version}) for {environment}"
            )

    if environment not in ["acc", "prd"]:
        return Git().rev_parse("--short", "HEAD").strip()

    current_commit_tags = Git().tag("--points-at", "HEAD").splitlines()
    for tag_version in current_commit_tags:
        if validate_version(environment, version):
            return tag_version

    if environment == "acc":
        raise click.UsageError(
            f"Could not get valid version tag for ACC on current commit ({current_commit_tags}), valid format is: <major>.<minor>.<patch>rc<number>"  # noqa: E501
        )
    elif environment == "prd":
        raise click.UsageError(
            f"Could not get valid version tag for PRD on current commit ({current_commit_tags}), valid format is: <major>.<minor>.<patch>"  # noqa: E501
        )


def validate_version(environment, version):
    try:
        version = version_parser(version.strip())
    except (IndexError, InvalidVersion):
        return False

    if environment == "acc" and version.pre:
        return True
    elif environment == "prd" and not (
        version.pre or version.post or version.dev or version.local
    ):
        return True
    elif environment in ["acc", "prd"]:
        return False
    return True
