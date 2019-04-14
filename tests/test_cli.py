import pytest
from click.testing import CliRunner
from cron2db import cli, CronDB
from tempfile import NamedTemporaryFile
from os import remove


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(scope="module")
def dummy_output():
    '''create dummy output files'''
    se_tmp_content, so_tmp_content = b'stderr data', b'stdout data'
    se_tmp = _write_file(se_tmp_content)
    so_tmp = _write_file(so_tmp_content)
    yield ((se_tmp, se_tmp_content), (so_tmp, so_tmp_content))
    # remove temp files
    for f in se_tmp, so_tmp:
        remove(f.name)


def _write_file(f_content):
    '''write f_content to temp file & return it'''
    f = NamedTemporaryFile(delete=False)
    f.write(f_content)
    f.close()
    return f


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception


def test_add_from_files(dummy_output):
    ((se_tmp, se_tmp_content), (so_tmp, so_tmp_content)) = dummy_output
    status = 1
    cdb = CronDB(engine='sqlite:///:memory:')  # initialize blank DB
    cdb.add_from_files('testcron.sh', se_tmp.name, so_tmp.name, status)
    top_result = next(cdb.return_all())      # only one entry
    assert top_result.stderr == se_tmp_content.decode("utf-8")
    assert top_result.stdout == so_tmp_content.decode("utf-8")
    assert top_result.status == 1

# def test_cli(runner):
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     assert not result.exception
#     assert result.output.strip() == 'Hello, world.'


# def test_cli_with_option(runner):
#     result = runner.invoke(cli.main, ['--as-cowboy'])
#     assert not result.exception
#     assert result.exit_code == 0
#     assert result.output.strip() == 'Howdy, world.'


# def test_cli_with_arg(runner):
#     result = runner.invoke(cli.main, ['James'])
#     assert result.exit_code == 0
#     assert not result.exception
#     assert result.output.strip() == 'Hello, James.'
