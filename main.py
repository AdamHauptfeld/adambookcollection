#Adam's Book Collection Interactive Webapp
#py -m streamlit run main.py
#https://adambookcollection.streamlit.app/

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from dashboard import dashboard
from dataset_viewer_v1 import dataset_viewer


st.set_page_config(page_title = "Adam Hauptfeld", page_icon="📚", layout="wide", initial_sidebar_state="expanded",)


def main():
    book_table = pd.read_csv(r"adam_book_collection.csv")
    
    with st.sidebar:
        selected_page = option_menu(
            menu_title = None, 
            options = ['Dashboard', 'The Collection', 'About the Project'],
            icons = ['graph-up', 'star', 'book'],
            default_index=0
        )
        st.markdown('<a href="mailto:adam.h.analytics@gmail.com">Email Me</a>', unsafe_allow_html=True)
    
    if selected_page == 'Dashboard':
        dashboard(book_table)

    if selected_page == 'The Collection':
        dataset_viewer(book_table)

    if selected_page == 'About the Project':
        st.title("Adam Hauptfeld")
        st.title("About the Project")
        st.caption('“Collect books, even if you don\'t plan on reading them right away. Nothing is more important than an unread library.”')
        st.caption('-John Waters')
        st.header('I Love My Books')
        lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
        reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in \
        culpa qui officia deserunt mollit anim id est laborum."
        st.write(lorem_ipsum)
        st.header('Project Challenges')
        st.write(lorem_ipsum)
        st.header('What I Learned')
        st.write(lorem_ipsum)

    
main()

    # if selected_page == 'Visualizations':
    #     st.title("Adam's Book Collection")
    #     pie_charts(book_table)

    # if selected_page == 'Filter and Aggregate':
    #     st.title("Adam's Book Collection")
    #     st.subheader("Let's find some numbers:")
    #     perform_and_display_aggregations(book_table)

    # if selected_page == 'Make-a-Viz':
    #     st.title("Adam's Book Collection")
    #     st.write("Under construction.")


# def pie_charts(dataframe):
#     # Pie chart of fiction and non-fiction books
#     st.subheader("What percentage of my collection is fiction vs. non-fiction?")
#     data = {"Type": [" Fiction", " Non-Fiction"], "Count" : [(dataframe['fiction'] == 1).sum(), (dataframe['fiction'] == 0).sum()]}
#     fiction_non_fiction_count_df = pd.DataFrame(data)
    
#     fiction_nonfiction_chart = plot.pie(fiction_non_fiction_count_df, names = "Type", values = "Count")

#     st.plotly_chart(fiction_nonfiction_chart)

#     # Pie chart of read by Adam
#     st.subheader("How many of my books have I actually read?")
#     data = {"Have I read it?": [" Finished it.", " I've read about half of it.", " I haven't read it yet."],\
#             "Count" : [(dataframe['read_by_adam'] == 2).sum(),\
#                         (dataframe['read_by_adam'] == 1).sum(), \
#                         (dataframe['read_by_adam'] == 0).sum()]}
#     read_by_adam_df = pd.DataFrame(data)
#     read_chart = plot.pie(read_by_adam_df, names = "Have I read it?", values = "Count")
#     st.plotly_chart(read_chart)



# #Perform some aggregations on the table
# def perform_and_display_aggregations(dataframe):
#     filtered_table, selected_dimension = (table_dimension_filterer(dataframe))
    
#     agg_results, selected_measure, selected_agg, selected_title  = table_aggregator(filtered_table)

#     if selected_measure == 'Titlecount':
#         if selected_dimension == 'N/A - Use the whole table':
#             display_message = str("There are " + str(agg_results) + " total titles in my collection.")
#             st.markdown(f"""
#             ##### {display_message}
#             """)
#         else:
#             display_message = str("There are " + str(agg_results) + " total " + selected_dimension.lower() + " titles in my collection.")
#             st.markdown(f"""
#             ##### {display_message}
#             """)
#     if selected_measure == 'Completed Count':
#         if selected_dimension == 'N/A - Use the whole table':
#             display_message = str('I have finished reading ' + str(agg_results) + " of my books.")
#             st.markdown(f"""
#             ##### {display_message}
#             """)
#         else:
#             display_message = str('I have finished reading ' + str(agg_results) + " of the " + selected_dimension.lower() + \
#                                 " titles in my collection.")
#             st.markdown(f"""
#             ##### {display_message}
#             """)
#     elif selected_measure == 'Pages':
#         if selected_title is None:
#             if selected_dimension == 'N/A - Use the whole table':
#                 display_message = str('The ' + selected_agg + ' of the pages for my whole collection is ' + str(agg_results) + ".")
#                 st.markdown(f"""
#             ##### {display_message}
#             """)
#             else:
#                 display_message = str('The ' + selected_agg.lower() + ' of the pages of the ' + selected_dimension.lower() +\
#                                     ' books in my collection is ' + str(agg_results) + ".")
#                 st.markdown(f"""
#             ##### {display_message}
#             """)
#         else:
#             if selected_dimension == 'N/A - Use the whole table':
#                 display_aggregate_message = str('The ' + selected_agg.lower() + ' pages for a book in my collection is ' + \
#                         str(agg_results) + ".")
#                 display_title_message = str('The book with the ' + selected_agg.lower() + ' number of pages is "' + \
#                         selected_title + '."')
#                 st.markdown(f"""
#             ##### {display_aggregate_message}
#             """)
#                 st.markdown(f"""
#             ##### {display_title_message}
#             """)
#                 if st.button("View title entry:"):
#                     filtered_dataframe = dataframe[dataframe['title'] == selected_title]
#                     st.write(filtered_dataframe)
#                     if st.button("Clear"):
#                         st.button("View title entry:") == False
#                 # formatted_title = selected_title.replace(' ', '+')
#                 # url = f"https://bookshop.org/search?keywords={formatted_title}"
#                 # st.write(f'<a href="{url}" target="_blank">Buy the book</a>', unsafe_allow_html=True)
#             else:
#                 display_aggregate_message = str('The ' + selected_agg.lower() + ' pages for a ' + selected_dimension.lower() + ' title in my collection is ' + \
#                         str(agg_results) + ".")
#                 display_title_message = str('The '+ selected_dimension.lower() + ' title with the ' + selected_agg.lower() + ' number of pages is "' + \
#                         selected_title + '."')
#                 st.markdown(f"""
#             ##### {display_aggregate_message}
#             """)
#                 st.markdown(f"""
#             ##### {display_title_message}
#             """)
#                 if st.button("View title entry:"):
#                     filtered_dataframe = dataframe[dataframe['title'] == selected_title]
#                     st.write(filtered_dataframe)
#                     if st.button("Clear"):
#                         st.button("View title entry:") == False
#                 # formatted_title = selected_title.replace(' ', '+')
#                 # url = f"https://bookshop.org/search?keywords={formatted_title}"
#                 # st.write(f'<a href="{url}" target="_blank">Buy the book</a>', unsafe_allow_html=True)
#     elif selected_measure == 'Year':
#         if selected_title is None:
#             if selected_dimension == 'N/A - Use the whole table':
#                 display_message = str('The ' + selected_agg.lower() + ' for a title in my collection is ' + str(agg_results) + ".")
#                 st.markdown(f"""
#             ##### {display_message}
#             """)
#             else:
#                 display_message = str('The ' + selected_agg.lower() + ' for the ' + selected_dimension.lower() +\
#                                     ' titles in my collection is ' + str(agg_results) + ".")
#                 st.markdown(f"""
#             ##### {display_message}
#             """)
#         else:
#             if selected_dimension == 'N/A - Use the whole table':
#                 display_aggregate_message = str('The ' + selected_agg.lower() + ' published book in my collection is ' + \
#                         str(agg_results) + ".")
#                 display_title_message = str('The book with the ' + selected_agg.lower() + ' year of publication is "' + \
#                         selected_title + '."')
#                 st.markdown(f"""
#             ##### {display_aggregate_message}
#             """)
#                 st.markdown(f"""
#             ##### {display_title_message}
#             """)
#                 if st.button("View title entry:"):
#                     filtered_dataframe = dataframe[dataframe['title'] == selected_title]
#                     st.write(filtered_dataframe)
#                     if st.button("Clear"):
#                         st.button("View title entry:") == False
#                 # formatted_title = selected_title.replace(' ', '+')
#                 # url = f"https://bookshop.org/search?keywords={formatted_title}"
#                 # st.write(f'<a href="{url}" target="_blank">Buy the book</a>', unsafe_allow_html=True)
#             else:
#                 display_aggregate_message = str('The ' + selected_agg.lower() + ' published ' + selected_dimension.lower() + ' book in my collection is ' + \
#                             str(agg_results) + ".")
#                 display_title_message = str('The ' + selected_dimension.lower() + ' book with the ' + selected_agg.lower() + ' year of publication is "' + \
#                         selected_title + '."')
#                 st.markdown(f"""
#             ##### {display_aggregate_message}
#             """)
#                 st.markdown(f"""
#             ##### {display_title_message}
#             """)
#                 if st.button("View title entry:"):
#                     filtered_dataframe = dataframe[dataframe['title'] == selected_title]
#                     st.write(filtered_dataframe)
#                     if st.button("Clear"):
#                         st.button("View title entry:") == False
#                 # formatted_title = selected_title.replace(' ', '+')
#                 # url = f"https://bookshop.org/search?keywords={formatted_title}"
#                 # st.write(f'<a href="{url}" target="_blank">Buy the book</a>', unsafe_allow_html=True)


#Pick any column and a value found in that column
# st.subheader("Filter Data")
# columns = book_table.columns.tolist()
# selected_column = st.selectbox("Select column to filter by", columns)
# unique_values = book_table[selected_column].unique()
# selected_value = st.selectbox("Choose", unique_values)

#Create a table filtered by the selected value in that column and display it
# filtered_table = book_table[book_table[selected_column] == selected_value]
# st.write(filtered_table)

#Define X- and Y- Axis variables
# st.subheader("Select X and Y Axis")
# x_column = st.selectbox("Select x-axis column", columns)
# y_column = (st.selectbox("Select y-axis column", columns))

#Aggregate (sum) the y-column by the x-column and display it
# table_grouped = book_table.groupby(x_column)[y_column].sum().reset_index()
# st.write(table_grouped)

#Create line chart of grouped table
# if st.button("Create Viz"):
#     st.line_chart(table_grouped.rename(columns={'original_copyright_year': 'index'}).set_index('index'))

