import click
from cron2db.db import CronDB, Config


@click.command()
@click.option('--cmd', help='cmd with arguments')
@click.option('--stderr', help='Path to stderr file')
@click.option('--stdout', help='Path to stdout file')
@click.option('--start', help='start time (epoch seconds)', type=int)
@click.option('--end', help='start time (epoch seconds)', type=int)
@click.option('--rc', help='return code', type=int)
@click.argument('mode', default='add')
def main(mode, cmd, stderr, stdout, rc, start, end):
    """Store cron results in a database"""
    cf = Config()
    cj = CronDB(engine=cf.config['cron2db']['database'])
    if mode == 'list':
        print(list(cj.return_all()))
    elif mode == 'add':
        cj.add(cmd, stderr, stdout, rc, start, end)
    elif mode in ('init', 'initialize'):
        pass
    else:
        raise ValueError
