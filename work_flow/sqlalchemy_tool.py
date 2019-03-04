from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,Date
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(name)s | %(levelname)s | %(message)s') #logging 使用前需要先做基本设置
logger = logging.getLogger(__name__) #这步不是很懂

class order_orm():
    def __init__(self,db,driver,user,passwd,host,port,schema):
        self.uri = '%s+%s://%s:%s@%s:%s/%s' % (db,driver,user,passwd,host,port,schema)
        logger.info('Connecting to : '+self.uri)
        self.engine = create_engine(self.uri)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
        self.Base = declarative_base()
    def db_init(self):
        class order_list(self.Base):
            __tablename__ = 'work_flow_order_list'
            openid = Column(String(50),nullable=True)
            user_name = Column(String(100),nullable=True)
            uuid = Column(String(50),primary_key=True)
            client = Column(String(100))
            order_dt = Column(Date())
            sub_dt = Column(Date())
            order_quantity = Column(String(100)) #数量
            spec = Column(String(200)) #规格
            unit = Column(String(100)) ##单位
            order_status = Column(Integer)
            person_incharge = Column(String(100))
            company = Column(String(100))
            requirement = Column(String(200)) #用纸要求
            remark = Column(String(100)) #备注
            next_node = Column(String(100),default='暂无')

        class order_stat(self.Base):
            __tablename__ = 'work_flow_order_stat'
            stat_cd = Column(Integer(),primary_key=True)
            stat_name = Column(String(20))

        self.Base.metadata.create_all(self.engine)



if __name__ == '__main__':
    db = order_orm('mysql','pymysql','root','root','47.107.119.21','3306','test')
    db.db_init()
    db.session.commit()
    db.session.close()
