import click
from cron2db.db import CronDB, Config


@click.command()
@click.option('--as-cowboy', '-c', is_flag=True, help='Greet as a cowboy.')
@click.option('--stderr', help='Path to stderr file')
@click.option('--stdout', help='Path to stdout file')
@click.argument('mode', default='list', required=True)
def main(mode, stderr, stdout, as_cowboy):
    """Store cron results in a database"""
    # greet = 'Howdy' if as_cowboy else 'Hello'
    # click.echo('{0}, {1}.'.format(greet, name))
    cf = Config()
    cj = CronDB(engine=cf.config['cron2db']['database'])
    if mode == 'list':
        cj.add('ls', '', 'ok', 0, 100, 200)
        print(list(cj.return_all()))
    elif mode == 'add':
        pass
