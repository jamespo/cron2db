import configparser
import datetime
import platform
import os.path
from cron2db.version import __version__
from sqlalchemy import create_engine, Column, Integer, String, DateTime, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class MetaData(Base):
    '''metadata inc version # etc'''
    __tablename__ = 'metadata'

    key = Column(String(30), primary_key=True)
    value = Column(String(30))


class CronJob(Base):
    '''store cron results'''
    __tablename__ = 'cronjobs'

    id = Column(Integer, primary_key=True)
    job = Column(String(100))
    stderr = Column(String(500))
    stdout = Column(String(500))
    status = Column(Integer)
    start = Column(DateTime)
    end = Column(DateTime)
    hostname = Column(String(60), default=platform.node())

    def __repr__(self):
        return '<Job %r>' % self.job

    def __str__(self):
        return "Job: %s\nStart: %s\nEnd: %s\nStdout: %s\nStderr: %s" % \
            (self.job, self.start, self.end, self.stdout, self.stderr)


class CronDB():
    '''high level DB operations'''
    def __init__(self, engine):
        self.engine = create_engine(engine)
        self.Session = sessionmaker(bind=self.engine)
        # check if schema exists, create if not
        try:
            assert self.get_conf_entry('version') == __version__
        except exc.OperationalError:
            self._create_schema()

    def _create_schema(self):
        '''create DB schema'''
        Base.metadata.create_all(self.engine)  # create tables
        vers = MetaData(key='version', value=__version__)
        session = self.Session()
        session.add(vers)
        session.commit()

    def add(self, job, stderr, stdout, status, start_ep, end_ep):
        '''add cron results. start_ep & end_ep are epoch seconds'''
        cr = CronJob(job=job, stderr=stderr, stdout=stdout, status=status,
                     start=datetime.datetime.fromtimestamp(start_ep),
                     end=datetime.datetime.fromtimestamp(end_ep))
        session = self.Session()
        session.add(cr)
        session.commit()

    def add_from_files(self, job, stderr_file, stdout_file, status,
                       start_ep, end_ep):
        '''load cron results from temp output files'''
        with open(stderr_file) as se:
            stderr = se.read()
        with open(stdout_file) as so:
            stdout = so.read()
        self.add(job, stderr, stdout, status, start_ep, end_ep)

    def return_all(self):
        '''return all jobs as iterator'''
        session = self.Session()
        for instance in session.query(CronJob):
            yield instance

    def get_conf_entry(self, confkey):
        '''get entry from metadata table'''
        session = self.Session()
        res = session.query(MetaData.value).filter_by(key=confkey)[0:1]
        return res[0].value


class Config():
    '''parse config'''
    def __init__(self, conf=None):
        '''load the config, local overrides global'''
        self.config = configparser.ConfigParser()
        if conf is not None:
            confpaths = [conf]  # custom confpath
        else:
            homeconf = os.path.join(os.path.expanduser('~'), '.config', 'cron2db.conf')
            confpaths = ['/etc/cron2db.conf', homeconf]
        confs = self.config.read(confpaths)
        if len(confs) == 0:
            # no conf - write barebones
            self._barebones_conf()

    def _barebones_conf(self):
        self.config = configparser.ConfigParser()
        homedir = os.path.expanduser('~')
        homeconf = os.path.join(homedir, '.config', 'cron2db.conf')
        dbpath = os.path.join(homedir, '.config', 'cron2db.sqlite')
        self.config['cron2db'] = {}
        self.config['cron2db']['database'] = 'sqlite:///' + dbpath
        with open(homeconf, 'w') as configfile:
            self.config.write(configfile)
