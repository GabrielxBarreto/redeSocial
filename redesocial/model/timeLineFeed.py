class TimeLineFeed:
    count = 0 
    def __init__(self,user,posts_list,midia_list,description):
        TimeLineFeed.count += 1
        self.id = TimeLineFeed.count
        self.__user = user
        self.__posts_list = posts_list
        self.__midia_list = midia_list
        self.__description = description
    @property
    def user(self):
        return self.__user
    @user.setter
    def user(self,new_user):
        self.__user = new_user

    @property
    def posts_list(self):
        return self.__posts_list
    @posts_list.setter
    def posts_list(self,post_list):
        self.__posts_list = post_list

    @property
    def midia_list(self):
        return self.__midia_list
    @midia_list.setter
    def midia_list(self,midia_list):
        self.__midia_list = midia_list

    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self,description):
        self.__description = description
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.__user.id,
            "posts_list": [p.id for p in self.__posts_list],
            "midia_list": [m.id for m in self.__midia_list],
            "description": self.__description
        }



