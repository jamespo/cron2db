from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class CronJob(Base):
    '''store cron results'''
    __tablename__ = 'cronjobs'

    id = Column(Integer, primary_key=True)
    job = Column(String(100))
    stderr = Column(String(500))
    stdout = Column(String(500))
    status = Column(Integer)

    # def __init__(self, job, stdout, stderr, status):
    #     self.job = job
    #     self.stdout = stdout
    #     self.stderr = stderr
    #     self.status = status

    def __repr__(self):
        return '<Job %r>' % self.job


class CronDB():

    def __init__(self, engine='sqlite:///:memory:'):
        self.engine = create_engine(engine)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)  # create tables

    def add(self, job, stderr, stdout, status):
        '''add cron results'''
        cr = CronJob(job=job, stderr=stderr, stdout=stdout, status=status)
        session = self.Session()
        session.add(cr)
        session.commit()

    def add_from_files(self, job, stderr_file, stdout_file, status):
        '''load cron results from temp output files'''
        with open(stderr_file) as se:
            stderr = se.read()
        with open(stdout_file) as so:
            stdout = so.read()
        self.add(job, stderr, stdout, status)

    def return_all(self):
        '''return all jobs as iterator'''
        session = self.Session()
        for instance in session.query(CronJob):
            yield instance
