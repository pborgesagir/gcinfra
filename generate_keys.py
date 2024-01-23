import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Peter Parker", "Rebecca Miller", "Pedro Borges", "Arthur Pires", "Kaio Razotto", "Vitor Peixoto", "Claudemiro Dourado", "Izabela Lopes", "Fernando Souza", "Michelle Bonfim"]
usernames = ["pparker", "rmiller", "pborges", "arthur.pires", "kaio.razotto", "vitor.peixoto", "claudemiro.dourado", "izabela.lopes", "fernando.souza", "michelle.bonfim"]
passwords = ["XXX", "XXX", "agirabc", "Agir@2024", "Agir@2024", "Agir@2024", "Agir@2024", "Agir@2024", "Agir@2024" ]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
