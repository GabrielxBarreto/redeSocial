from ..data.userData import user_df
from ..data.publicationData import publication_df
from ..data.midiaData import midia_df
from ..data.projectsData import projects_df

from ..model.publication import Publication
from ..model.projects import Projects

from ..model.midia import Midia
from datetime import datetime, date

#----teste---
import tkinter as tk
from tkinter import filedialog
from PIL import Image
#--------------
import os
import re
def createTimeLine(session):
    result = user_df[user_df["id"] == session]
    print("who am I?____________________________")
    print(result.iloc[0]["id"])
    print(result.iloc[0]["name"])
    print(result.iloc[0]["email"])
    print("feed________________________________")
    print(result.iloc[0]["post_list"])
    print(result.iloc[0]["tags"])

    new_post(session)
    name = input("quem você deseja seguir (Digite o nome): ")
    if user_df[user_df["name"]] == name:
        user_df[user_df["followers"]]
#user_df.loc[user_df["name"] == "Gabriel", "tags"].iloc[0].append("python")
#adicionando valores
def new_post(session,archive,description):
    result = user_df[user_df["id"] == session]
    tags = re.findall(r"#\w+",description)
    idx = user_df.index[user_df["id"] == session][0]
    user_tags = user_df.at[idx, "tags"]
    user_tags.extend(tags)
    

    archive = filedialog.askopenfilename(
    title="Selecione uma imagem",
    filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )

    img = Image.open(archive)
    format = img.format
    size_bytes =  os.path.getsize(archive)
    name_content = os.path.basename(archive)
    user_df.at[idx, "tags"] = user_tags
    
    type = "text"
    midia = Midia(format,size_bytes, name_content, archive, result.iloc[0]["id"],None)
    
    day = datetime.now().strftime("%H:%M:%S")
    times = datetime.now().strftime("%I:%M %p")
    
    publication = Publication(type, [midia], description, result.iloc[0]["id"],tags,day,times)
    midia.id_publication = publication.id

    publication_df.loc[len(publication_df)] = publication.to_dict()
    user_post = user_df.at[idx, "post_list"]
    user_post.extend(publication.to_dict())
    user_df.at[idx, "post_list"] = user_post
    midia_df.loc[len(midia_df)] = midia.to_dict()
    print("________________________________________________-")
    print(publication_df)

def excluirPost():
    pass
def publish_project(session,author,title,link_github,description):

    result = user_df[user_df["id"] == session]
    result["id"].values[0]
    project = Projects(title.get(),author.get(),session,link_github.get(),description.get())
    projects_df.loc[len(projects_df)]=project.to_dict()
    print(projects_df)

def like_post(id_post,id_user):
    publication_df.loc[publication_df["id"]==id_post,"like_counter"] += 1
    print(publication_df[publication_df["id"]==id_post])

def coment(id_user,text):
    print(id_user)
    print(text)
