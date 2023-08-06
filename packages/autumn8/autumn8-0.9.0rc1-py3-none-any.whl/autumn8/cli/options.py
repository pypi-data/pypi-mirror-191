import click
from questionary import Choice
import questionary

from autumn8.cli.cli_environment import CliEnvironment
from autumn8.cli.interactive import (
    pick_organization_id,
    verify_organization_id_access,
)
from autumn8.common.config.settings import CloudServiceProvider
from autumn8.common.config.supported_instances import find_instance_config

ENABLE_TOGGLEABLE_ENVIRONMENT = True


def use_environment(func):
    allowed_environments = (
        [env.name for env in CliEnvironment]
        if ENABLE_TOGGLEABLE_ENVIRONMENT
        else [CliEnvironment.PRODUCTION.name]
    )

    return click.option(
        "-e",
        "--environment",
        "--env",
        is_eager=True,  # often used when evaluating other options
        type=click.Choice(allowed_environments, case_sensitive=False),
        default=CliEnvironment.PRODUCTION.name,
        callback=lambda c, p, v: getattr(CliEnvironment, v),
        help="Environment to use",
        hidden=True,
    )(func)


def pick_or_verify_organization(ctx, param, value):
    organization_id = value
    environment = ctx.params["environment"]

    if organization_id is None:
        return pick_organization_id(environment)
    else:
        verify_organization_id_access(environment, organization_id)
        return value


use_organization_id = click.option(
    "-o",
    "--organization_id",
    "--org_id",
    type=int,
    callback=pick_or_verify_organization,
    help="The ID of the Organization to use",
)


def pick_cloud_provider(options):
    cloud_provider = questionary.select(
        "Choose service provider",
        choices=[Choice(provider) for provider in options],
        use_shortcuts=True,
    ).unsafe_ask()
    return cloud_provider


def pick_valid_cloud_provider(ctx, param, value):
    machine_type = ctx.params["machine_type"]
    if value:
        return value
    # organization_id = value
    # environment = ctx.params["environment"]
    instance_config = find_instance_config(
        machine_type, fetch_data_from_cloud_info=False
    )

    valid_providers = (
        instance_config.service_provider,
        CloudServiceProvider.AUTUMN8,
    )

    return pick_cloud_provider(valid_providers)


def use_cloud_provider_picker(prompt=True):
    return click.option(
        "-c",
        "--cloud_provider",
        type=click.Choice(
            [provider.name for provider in CloudServiceProvider],
            case_sensitive=False,
        ),
        callback=pick_valid_cloud_provider,
        help="Cloud provider to use",
    )
