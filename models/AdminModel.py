from database.db import db
from enums.AdminEnum import AdminEnum

class AdminModel(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    @property
    def level_name(self) -> str:
        return AdminEnum.from_level(self.level)
    
    def __repr__(self):
        return f'<Admin(name={self.name}, email={self.email}, level={self.level})>'