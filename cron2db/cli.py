import click
import time
from cron2db.db import CronDB, Config

epoch_time = int(time.time())

@click.command()
@click.argument('mode', default='add',
                type=click.Choice(['add', 'ls', 'init']))
@click.option('--cmd', help='cmd with arguments')
@click.option('--stderr', help='Path to stderr file', default='')
@click.option('--stdout', help='Path to stdout file', default='')
@click.option('--start', help='start time (epoch seconds)', type=int,
              default=epoch_time)
@click.option('--end', help='end time (epoch seconds)', type=int,
              default=epoch_time)
@click.option('--rc', help='return code', type=int, default=-1)
def main(mode, cmd, stderr, stdout, rc, start, end):
    """Store cron results in a database"""
    cf = Config()
    cj = CronDB(engine=cf.config['cron2db']['database'])
    if mode == 'ls':
        for job in cj.return_all():
            print(job, "\n")
        # print(list(cj.return_all()))
    elif mode == 'init':
        pass
    elif mode == 'add' and cmd is not None:
        cj.add_from_files(cmd, stderr, stdout, rc, start, end)
    else:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()
