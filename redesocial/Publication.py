from Midia import Midia
class Publication:
    count = 0 
    def __init__(self, type, midia_list:list[Midia], description, user):
        
        Publication.count += 1
        self.id = Publication.count
        self._type = type
        self._midia_list = midia_list
        self._description = description
        self._user = user

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        self._type = new_type

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

m = Midia("foto",50000,"sweet dreams","/who/am/i/to/desagree/sweet dreams.png")
p = Publication("text",[],"Testando apenas",1)
p.midia_list.append(m)
p.midia_list.append(m)
p.midia_list.append(m)

print(p.midia_list[1].id)

