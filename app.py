import os
import pandas as pd
import streamlit as st
from datetime import datetime




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
    st.success("✅ Attendance Successfully Saved!")





