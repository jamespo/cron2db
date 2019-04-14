import click
from cron2db import CronDB


@click.command()
@click.option('--as-cowboy', '-c', is_flag=True, help='Greet as a cowboy.')
@click.argument('name', default='world', required=False)
def main(name, as_cowboy):
    """Store cron results in a database"""
    greet = 'Howdy' if as_cowboy else 'Hello'
    click.echo('{0}, {1}.'.format(greet, name))
    cj = CronDB()
    cj.add('ls', '', 'ok', 0)
    print(list(cj.return_all()))
