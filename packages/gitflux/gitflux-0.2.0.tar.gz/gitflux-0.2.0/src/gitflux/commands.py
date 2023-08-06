import click
from github import Github, AuthenticatedUser, Organization


def parse_repo_fullname(user: AuthenticatedUser, orgs: list[Organization], fullname: str) -> tuple:
    if fullname.find('/') == -1:
        owner = user
        repo_name = fullname
    else:
        org_name, repo_name = fullname.split('/')
        owner = next((x for x in orgs if x.login == org_name), None)

        if owner is None:
            raise NameError(f'Organization not found: {org_name}.')

    return owner, repo_name


@click.command('list-repos')
@click.pass_context
def list_repos_command(ctx: click.Context):
    """List all remote repositories."""

    github: Github = ctx.obj['github']

    for repo in github.get_user().get_repos():
        click.echo(repo.full_name)


@click.command('create-repos')
@click.argument('names', required=True, nargs=-1)
@click.pass_context
def create_repos_command(ctx: click.Context, names: tuple[str]):
    """Create remote repositories."""

    github: Github = ctx.obj['github']

    user = github.get_user()
    orgs = user.get_orgs()

    for name in names:
        owner, repo_name = parse_repo_fullname(user, orgs, name)
        owner.create_repo(repo_name)


@click.command('delete-repos')
@click.argument('names', required=True, nargs=-1)
@click.pass_context
def delete_repos_command(ctx: click.Context, names: tuple[str]):
    """Delete an existing repository."""

    github: Github = ctx.obj['github']

    user = github.get_user()
    orgs = user.get_orgs()

    for name in names:
        owner, repo_name = parse_repo_fullname(user, orgs, name)
        owner.get_repo(repo_name).delete()
