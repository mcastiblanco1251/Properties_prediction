import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names=['Manuel Castiblanco', 'Pedro Gomez']
usernames=['mcastiblanco', 'pgomez']
paswords=['abc123','def456']

hashed_paswords=stauth.Hasher(paswords).generate()
file_path= Path(__file__).parent/'hashed_pw.pkl'

with file_path.open('wb') as file:
    pickle.dump(hashed_paswords,file)
