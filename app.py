import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import numpy as np
import datetime
import re

pd.options.mode.chained_assignment = None

def dataframe_with_selections(df, inp_key):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=False)},
        disabled=df.columns,
        key=inp_key,
        use_container_width=True,
    )
    selected_indices = list(np.where(edited_df.Select)[0])
    selected_rows = df[edited_df.Select]
    return {"selected_rows_indices": selected_indices, "selected_rows": selected_rows}

st.header('Handbags Stock\n')

df = pd.read_csv('Handbags July 2025 No Groups.csv')
df['Colour'] = df['Colour'].str.capitalize()

temp = df.groupby(['Style'])[['Stock', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Total']].sum().reset_index().sort_values(by='Stock', ascending=False).reset_index(drop=True)

selection = dataframe_with_selections(temp, 1)

if (selection['selected_rows_indices'] != []):

    selected_prod = temp.loc[selection['selected_rows_indices'][0]]['Style']
    df = df[df['Style'] == selected_prod]

    image_column, df_column = st.columns([0.2, 0.8])
    image_column.image(df.iloc[0]['Image'])
    df_column.dataframe(df[['Style', 'Colour', 'Sale Price', 'Stock', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Total']].sort_values(by='Stock', ascending=False).reset_index(drop=True))