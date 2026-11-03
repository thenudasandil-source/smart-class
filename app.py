import os
import pandas as pd
import streamlit as st
from datetime import datetime
from github import Auth,Github
os.makedirs("csv_files", exist_ok=True)

def upload_to_github(local, remote, token, repo_name):
  r = Github(auth=Auth.Token(token)).get_repo(repo_name)
  content = open(local, encoding="utf-8").read()

  try:
    f = r.get_contents(remote)
    r.update_file(f.path, "Update", content, f.sha)
  except:
    r.create_file(remote, "Create", content)

st.markdown(
    '<u><center><h1 style="color: white; font-weight: bold;">Class Attendance'
    " System</h1>",
    unsafe_allow_html=True,
)


now = datetime.now()
time = now.strftime("%Y-%m-%d")


gradeclass = st.selectbox("Select Grade", ["9-A", "9-B", "9-C", "9-D"])



file_name = f"{gradeclass}_students.csv"
df = pd.read_csv(file_name)
df["status"] = df["status"] == "Present"

edited_df = st.data_editor(
    df,
    column_config={
        "status": st.column_config.CheckboxColumn("Present?", default=False)
    },
    disabled=["students"],
    hide_index=True,
)


file=f"csv_files/{gradeclass}_{time}.csv"
folder_path = file

if st.button("Save Attendance"):
    edited_df.to_csv(file,index=False)



    if os.path.exists(folder_path):
        os.remove(file)
    edited_df.to_csv(file, index=False)
    upload_to_github(
        local=file,
        remote=f"data/{gradeclass}_{time}.csv",
        token="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",
        repo_name="thenudasandil-source/class-room-data",
    )

    st.success("✅ Attendance Successfully Saved!")
