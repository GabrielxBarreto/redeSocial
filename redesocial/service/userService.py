from ..data.userData import user_df
from ..data.publicationData import publication_df
from ..model.publication import Publication
from ..model.midia import Midia
def createTimeLine(session):
    result = user_df[user_df["id"] == session]
    print("who am I?____________________________")
    print(result.iloc[0]["id"])
    print(result.iloc[0]["name"])
    print(result.iloc[0]["email"])
    print("feed________________________________")
    print(result.iloc[0]["post_list"])
    print(result.iloc[0]["tags"])

    newPost(session)
    name = input("quem você deseja seguir (Digite o nome): ")
    if user_df[user_df["name"]] == name:
        user_df[user_df["followers"]]
#user_df.loc[user_df["name"] == "Gabriel", "tags"].iloc[0].append("python")
#adicionando valores
def newPost(session):
    result = user_df[user_df["id"] == session]
    txt = input("Digite o que está pensando sobre o mundo da tecnologia:\n")
    tagsTxt = input("Digite as tags (#tag separado por espaço): ")

    tags = tagsTxt.split()
    idx = user_df.index[user_df["id"] == session][0]
    user_tags = user_df.at[idx, "tags"]
    user_tags.extend(tags)

    
    user_df.at[idx, "tags"] = user_tags

    type = "text"
    midia = Midia("png",200000, "exemploFase2", "documents/redesocial/server/uploads", result.iloc[0]["id"])
    publication = Publication(type, [midia], txt, result.iloc[0]["id"], tags)
    publication_df.loc[len(publication_df)] = publication.to_dict()
    user_post = user_df.at[idx, "post_list"]
    user_post.extend(publication.to_dict())
    user_df.at[idx, "post_list"] = user_post


    print(txt)
    print(tags)

def excluirPost():
    pass
