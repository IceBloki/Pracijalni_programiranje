import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base
import gui.gui as g

Base = declarative_base()


db_engine = db.create_engine('sqlite:///db//Baza.db')
Session = sessionmaker(bind=db_engine)
session = Session()


class User(Base):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    pin = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)
    is_activ = db.Column(db.Boolean)

    def __init__(self, name, surname, pin, is_admin=False, is_activ=True):
        self.name = name
        self.surname = surname
        self.pin = pin
        self.is_admin = is_admin
        self.is_activ = is_activ

    def __str__(self):
        return("USER: " + " " + str(self.name) + " " + self.surname)
    


class Admin(User):
    __tablename__ = "admin"

    chosen_user = None

    admin_id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    def __init__(self, name, surname, pin):
        super().__init__(name, surname, pin, is_admin=True, is_activ=True)


    def __str__(self):
        return("ADMIN: " + " " + self.name + " " + self.surname)
    
    @classmethod
    def add_user(self):
        new_name = g.admin_window.e_name.get()
        new_surname = g.admin_window.e_surname.get()
        new_pin = str(g.admin_window.e_pin.get())
        new_is_admin = bool(g.admin_window.checkbox_var_admin.get())
        new_is_activ = bool(g.admin_window.checkbox_var_activ.get())

        user = User(name=new_name, surname=new_surname, pin=new_pin, is_admin=new_is_admin, is_activ=new_is_activ)
        session.add(user)

        session.commit()

    @classmethod
    def get_users(cls):
        users = session.query(User).all()
        return users

    @classmethod
    def delete_user(cls, user_id):
        user = session.query(User).filter_by(id=user_id).first()
        session.delete(user)
        session.commit()

    @classmethod
    def update_user(cls, user_id):
        user = session.query(User).filter_by(id=user_id).first()
        new_name = g.admin_window.e_name.get()
        new_surname = g.admin_window.e_surname.get()
        new_pin = str(g.admin_window.e_pin.get())
        new_is_admin = bool(g.admin_window.checkbox_var_admin.get())
        new_is_activ = bool(g.admin_window.checkbox_var_activ.get())
        
        if len(new_name) > 1:
            user.name = new_name
        elif len(new_surname) > 1:
            user.surname = new_surname
        elif len(new_pin) > 1:
            user.pin = new_pin
        
        user.is_admin = new_is_admin
        user.is_activ = new_is_activ
        session.commit()

    @classmethod
    def compare_pin(cls, user_pin):
        user = session.query(User).filter_by(pin=user_pin).first()
        return user
    

    
Base.metadata.create_all(bind=db_engine)

