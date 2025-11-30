from ..data.projectsData import projects_df

class Projects:
    count = 0 
    
    def __init__(self, title, author, id_author, link_github, description):
        Projects.count += 1 + len(projects_df)
        self.id = Projects.count
        
        self.__title = title
        self.__author = author
        self.__id_author = id_author
        self.__link_github = link_github
        self.__description = description
        self.__score = 0

    # ---------------------------
    # GETTERS e SETTERS
    # ---------------------------

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_title):
        self.__title = new_title

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, new_author):
        self.__author = new_author

    @property
    def id_author(self):
        return self.__id_author

    @id_author.setter
    def id_author(self, new_id_author):
        self.__id_author = new_id_author

    @property
    def link_github(self):
        return self.__link_github

    @link_github.setter
    def link_github(self, new_link):
        self.__link_github = new_link

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, new_description):
        self.__description = new_description

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, new_score):
        self.__score = new_score

    # ---------------------------
    # Conversor para dict
    # ---------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.__title,
            "author": self.__author,
            "author_id": self.__id_author,
            "link_github": self.__link_github,
            "description": self.__description,
            "score": self.__score
        }
