# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"Smoothie Order Form! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!"""
)

# Name Entry
name_on_order = st.text_input('Name on Smoothie')
st.write('Name on your Smoothie will be:', name_on_order)

# Selecting fruits from our fruits table
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# Populating the ingredients list with the fruits from the dataframe
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients', my_dataframe, max_selections=5
)

# If fruits are selected
if ingredients_list:
    ingredients_string = ''

    # Adds the selected fruits to the fruits string
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    # Writes the insert statement using the selected ingredients and name
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) 
    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button("Submit Order")

    # Inserts the data into the orders dataset
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered '+ name_on_order + '!', icon="✅")

