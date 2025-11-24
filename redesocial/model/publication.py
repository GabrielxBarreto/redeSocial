from ..model.midia import Midia
class Publication:
    count = 0 
    def __init__(self, type, midia_list:list[Midia], description, user,tags_list,day,times):
        
        Publication.count += 1
        self.id = Publication.count
        self._type = type
        self._midia_list = midia_list
        self._description = description
        self._user = user
        self._tags_list = tags_list
        self.day = day
        self.times = times

   
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        self._type = new_type

    @property
    def tags_list(self):
        return self._type

    @tags_list.setter
    def tags_list(self, tags_list):
        self._tags_list = tags_list

    @property
    def midia_list(self):
        return self._midia_list

    @midia_list.setter
    def midia_list(self, new_midia_list):
        self._midia_list = new_midia_list

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        self._description = new_description

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, new_user):
        self._user = new_user
    def to_dict(self):
        return {
            "id": self.id,
            "type": self._type,
            "midia_list": [m.to_dict() for m in self._midia_list],
            "description": self._description,
            "user": self._user,
            "tags_list": self._tags_list,
            "day": self.day,
            "times": self.times

        }


