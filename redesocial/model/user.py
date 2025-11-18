from ..model.publication import Publication
class User:
    count = 0 
    
    def __init__(self,name,email,password,birthday,birth_month,birth_year,gender,status,post_list:list[Publication],tags:list[str]):
        User.count += 1
        self.id = User.count
        self.__name = name
        self.__email = email
        self.__password = password
        self.__birthday = birthday
        self.__birth_month = birth_month
        self.__birth_year = birth_year
        self.__gender = gender
        self.__status = status
        self.__post_list = post_list
        self.__tags = tags
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,new_name):
        self.__name = new_name

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self,new_email):
        self.__email = new_email

    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self,new_password):
        self.__password = new_password

    @property
    def birthday(self):
        return self.__birthday
    
    @birthday.setter
    def birthday(self,new_birthday):
        self.__birthday = new_birthday
    
    @property
    def birth_month(self):
        return self.__birth_month
    
    @birth_month.setter
    def birth_month(self,new_birth_month):
        self.__birth_month = new_birth_month

    @property
    def birth_year(self):
        return self.__birth_year
    
    @birth_year.setter
    def birth_year(self,new_birth_year):
        self.__birth_year = new_birth_year

    @property
    def gender(self):
        return self.__gender
    
    @gender.setter
    def gender(self,new_gender):
        self.__gender = new_gender

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self,new_status):
        self.__status = new_status

    @property
    def post_list(self):
        return self.__post_list
    
    @post_list.setter
    def post_list(self,new_post_list):
        self.__post_list = new_post_list
    
    @property
    def tags(self):
        return self.__tags
    
    @tags.setter
    def tags(self,new_tags):
        self.__tags = new_tags
    #
    # Conversor de OBJ para dict
    # 
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.__name,
            "email": self.__email,
            "password": self.__password,
            "birthday": self.__birthday,
            "birth_month": self.__birth_month,
            "birth_year": self.__birth_year,
            "gender": self.__gender,
            "status": self.__status,
            "post_list": self.__post_list,
            "tags": self.__tags
        }

