from ..model.user import User
from ..model.publication import Publication
from ..data.admData import adm_df
class Adm(User):
    count = 0
    def __init__(self,name,email,password,birthday,birth_month,birth_year,gender,status,post_list:list[Publication],tags:list[str]):
        super.__init__(name,email,password,birthday,birth_month,birth_year,gender,status,post_list,tags)
        Adm.count += 1 + len(adm_df)
        self.id_adm = Adm.count
    @property
    def id_adm(self):
        return self.id_adm

    @id_adm.setter
    def id_adm(self, id_adm):
        self.id_adm = id_adm
    def to_dict(self):
        return {
            "id_adm": self.id_adm,
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