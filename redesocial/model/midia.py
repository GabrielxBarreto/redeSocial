class Midia:
    count = 0
    def __init__(self, type, size, name, original_path,id_user,id_publication):
        Midia.count += 1
        self.id = Midia.count
        self._type = type
        self._size = size
        self._name = name
        self._original_path = original_path
        self._id_user = id_user
        self.id_publication = id_publication

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        self._type = new_type
    
    @property
    def id_user(self):
        return self._id_user

    @id_user.setter
    def id_user(self, new_id_user):
        self._id_user = new_id_user

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def original_path(self):
        return self._original_path

    @original_path.setter
    def original_path(self, new_path):
        self._original_path = new_path

    def to_dict(self):
        return {
            "id": self.id,
            "type": self._type,
            "size": self._size,
            "name": self._name,
            "original_path": self._original_path,
            "id_user":self._id_user,
            "id_publication":self.id_publication
        }
