import click
from ape import project
from ape.cli import (
    NetworkBoundCommand,
    ape_cli_context,
    network_option,
    select_account,
    select_account,
)


@click.command(cls=NetworkBoundCommand)
@ape_cli_context()
@network_option()
def cli(cli_ctx, network):
    network = cli_ctx.provider.network.name
    print(f"Deploying to: {network}")
    if network == "foundry" or network.endswith("-fork"):
        account = cli_ctx.account_manager.test_accounts[0]
    else:
        account = select_account()

    account.deploy(project.SBT721, account.address)
