#!/usr/bin/env python3
#_*_coding:utf-8_*_

from sqlalchemy import create_engine,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship
from  sqlalchemy.orm import sessionmaker
from sqlalchemy import or_,and_
from sqlalchemy import func
from sqlalchemy_utils import ChoiceType,PasswordType


Base = declarative_base()
engine = create_engine("mysql+pymysql://root:root@localhost:3306/test")


BindHost2Group = Table('bindhost_2_group',Base.metadata,
    Column('bindhost_id',ForeignKey('bind_host.id'),primary_key=True),
    Column('group_id',ForeignKey('group.id'),primary_key=True),
)

BindHost2UserProfile = Table('bindhost_2_userprofile',Base.metadata,
    Column('bindhost_id',ForeignKey('bind_host.id'),primary_key=True),
    Column('uerprofile_id',ForeignKey('user_profile.id'),primary_key=True),
)

Group2UserProfile = Table('group_2_userprofile',Base.metadata,
    Column('userprofile_id',ForeignKey('user_profile.id'),primary_key=True),
    Column('group_id',ForeignKey('group.id'),primary_key=True),
)

class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(32),unique=True,nullable=False)
    password = Column(String(128),unique=True,nullable=False)
    groups = relationship('Group',secondary=Group2UserProfile)
    bind_hosts = relationship('BindHost',secondary=BindHost2UserProfile)

    def __repr__(self):
        return "<UserProfile(id='%s',username='%s')>" % (self.id,self.username)

class RemoteUser(Base):
    __tablename__ = 'remote_user'
    AuthTypes = [
        (u'ssh-passwd',u'SSH/Password'),
        (u'ssh-key',u'SSH/KEY'),
    ]
    id = Column(Integer,primary_key=True,autoincrement=True)
    auth_type = Column(ChoiceType(AuthTypes))
    username = Column(String(64),nullable=False)
    password = Column(String(255))

    __table_args__ = (UniqueConstraint('auth_type', 'username','password', name='_user_passwd_uc'),)

    def __repr__(self):
        return "<RemoteUser(id='%s',auth_type='%s',user='%s')>" % (self.id,self.auth_type,self.username)


class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer,primary_key=True,autoincrement=True)
    hostname = Column(String(64),unique=True,nullable=False)
    ip_addr = Column(String(128),unique=True,nullable=False)
    port = Column(Integer,default=22)
    bind_hosts = relationship("BindHost")
    def __repr__(self):
        return "<Host(id='%s',hostname='%s')>" % (self.id,self.hostname)

class Group(Base):
    __tablename__  = 'group'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(64),nullable=False,unique=True)
    bind_hosts = relationship("BindHost",secondary=BindHost2Group, back_populates='groups' )
    user_profiles = relationship("UserProfile",secondary=Group2UserProfile )

    def __repr__(self):
        return "<HostGroup(id='%s',name='%s')>" % (self.id,self.name)


class BindHost(Base):
    '''Bind host with different remote user,
       eg. 192.168.1.1 mysql passAbc123
       eg. 10.5.1.6    mysql pass532Dr!
       eg. 10.5.1.8    mysql pass532Dr!
       eg. 192.168.1.1 root
    '''
    __tablename__ = 'bind_host'
    id = Column(Integer,primary_key=True,autoincrement=True)
    host_id = Column(Integer,ForeignKey('host.id'))
    remoteuser_id = Column(Integer,ForeignKey('remote_user.id'))
    host = relationship("Host")
    remoteuser = relationship("RemoteUser")
    groups = relationship("Group",secondary=BindHost2Group,back_populates='bind_hosts')
    user_profiles = relationship("UserProfile",secondary=BindHost2UserProfile)

    __table_args__ = (UniqueConstraint('host_id', 'remoteuser_id', name='_bindhost_and_user_uc'),)

    def __repr__(self):
        return "<BindHost(id='%s',name='%s',user='%s')>" % (self.id,
                                                           self.host.hostname,
                                                           self.remoteuser.username
                                                                      )


Base.metadata.create_all(engine) #创建所有表结构

if __name__ == '__main__':
    SessionCls = sessionmaker(bind=engine) #创建与数据库的会话session class ,
                                           # 注意,这里返回给session的是个class,不是实例
    session = SessionCls()



    res = session.query(Host).filter(and_(Host.hostname.like("ub%"), Host.port > 20)).all()
    print("-->",res)











