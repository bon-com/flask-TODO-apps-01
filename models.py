from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

# ベースモデル作成
Base = declarative_base()

class User(Base):
    """ 利用者クラス """
    # テーブル名称
    __tablename__ = 'user'
    # カラム
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

class TodoCategory(Base):
    """ タスクカテゴリークラス """
    # テーブル名称
    __tablename__ = 'todo_category'
    # カラム
    id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)
    
class Todo(Base):
    """ タスククラス """
    # テーブル名称
    __tablename__ = 'todo'
    # カラム
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    memo = Column(Text)
    status = Column(Integer, default=0)
    due_date = Column(DateTime)
    category_id = Column(Integer, ForeignKey('todo_category.id')) 
    user_id = Column(Integer, ForeignKey('user.id')) 
    # リレーションプロパティ
    user = relationship("User", backref="todos")
    category = relationship("TodoCategory", backref="todos")
