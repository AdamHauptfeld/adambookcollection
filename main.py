
#Adam's Book Collection Interactive Webapp
#py -m streamlit run main.py
#https://adambookcollection.streamlit.app/

import streamlit as st
import pandas as pd
import plotly.express as plot
from streamlit_option_menu import option_menu
from table_manipulations import table_aggregator, table_dimension_filterer

# Disable the below if using the banner code
st.set_page_config(layout="wide")


# # Custom HTML/CSS for the banner
# custom_html = """
# <div class="banner">
#     <img src="https://img.freepik.com/premium-photo/wide-banner-with-many-random-square-hexagons-charcoal-dark-black-color_105589-1820.jpg" alt="Banner Image">
# </div>
# <style>
#     .banner {
#         width: 160%;
#         height: 200px;
#         overflow: hidden;
#     }
#     .banner img {
#         width: 100%;
#         object-fit: cover;
#     }
# </style>
# """
# # Display the custom HTML
# st.components.v1.html(custom_html)




def main():
    book_table = pd.read_csv(r"adam_book_collection_webapp_version.csv")
    
    with st.sidebar:
        selected_page = option_menu(
            menu_title = None, 
            options = ['The Dataset', 'About the project', 'Visualizations', 'Filter and Aggregate', 'Make-a-Viz'],
            icons = ['book', 'blockquote-left', 'graph-up', 'funnel', 'brush'],
            default_index=0
        )

    if selected_page == 'The Dataset':
        st.title("Adam's Book Collection")
        st.write("Select a title to view details or click a column title to sort.")
        st.write("You can also search for an entry or download the whole dataset as a csv.")
        book_table['original_copyright_year'] = book_table['original_copyright_year'].astype(str).str.replace(",", "")
        book_table.rename(columns={'original_copyright_year': 'year'}, inplace=True)

        #This displays the simplified table and also stores the row of any selection the user makes.
        selected_row = st.dataframe(book_table[['title', 'author', 'genre', 'year', 'keywords']],
        hide_index=True,
        on_select='rerun',
        selection_mode='single-row'
        ).selection


        #This handles displaying a selected title and generate a link to buy it.
        if selected_row and len(selected_row['rows']) > 0:
            row_index = selected_row['rows'][0]
            just_selected_row = book_table.iloc[row_index:row_index+1]
            
            # Display the filtered row
            st.markdown("""
            ##### Selected Row Details
            """)
            st.write(just_selected_row)

            #Generate purchase link
            selected_title = just_selected_row['title'].iloc[0]
            selected_author = just_selected_row['author'].iloc[0]
            formatted_title = selected_title.replace(' ', '+')
            formatted_author = selected_author.replace(' ', '+')
            url = f"https://bookshop.org/search?keywords={formatted_title}+{formatted_author}"
            st.write(f'<a href="{url}" target="_blank">Buy {selected_title} by {selected_author} on Bookshop.org</a>', unsafe_allow_html=True)
    

    if selected_page == 'About the project':
            st.title("Adam's Book Collection")
            st.write("Under construction.")

    if selected_page == 'Visualizations':
        st.title("Adam's Book Collection")
        pie_charts(book_table)

    if selected_page == 'Filter and Aggregate':
        st.title("Adam's Book Collection")
        st.subheader("Let's find some numbers:")
        perform_and_display_aggregations(book_table)

    if selected_page == 'Make-a-Viz':
        st.title("Adam's Book Collection")
        st.write("Under construction.")


def pie_charts(dataframe):
    # Pie chart of fiction and non-fiction books
    st.subheader("What percentage of my collection is fiction vs. non-fiction?")
    data = {"Type": [" Fiction", " Non-Fiction"], "Count" : [(dataframe['fiction'] == 1).sum(), (dataframe['fiction'] == 0).sum()]}
    fiction_non_fiction_count_df = pd.DataFrame(data)
    
    fiction_nonfiction_chart = plot.pie(fiction_non_fiction_count_df, names = "Type", values = "Count")

    st.plotly_chart(fiction_nonfiction_chart)

    # Pie chart of read by Adam
    st.subheader("How many of my books have I actually read?")
    data = {"Have I read it?": [" Finished it.", " I've read about half of it.", " I haven't read it yet."],\
            "Count" : [(dataframe['read_by_adam'] == 2).sum(),\
                        (dataframe['read_by_adam'] == 1).sum(), \
                        (dataframe['read_by_adam'] == 0).sum()]}
    read_by_adam_df = pd.DataFrame(data)
    read_chart = plot.pie(read_by_adam_df, names = "Have I read it?", values = "Count")
    st.plotly_chart(read_chart)



#Perform some aggregations on the table
def perform_and_display_aggregations(dataframe):
    filtered_table, selected_dimension = (table_dimension_filterer(dataframe))
    
    agg_results, selected_measure, selected_agg, selected_title  = table_aggregator(filtered_table)

    if selected_measure == 'Titlecount':
        if selected_dimension == 'N/A - Use the whole table':
            display_message = str("There are " + str(agg_results) + " total titles in my collection.")
            st.markdown(f"""
            ##### {display_message}
            """)
        else:
            display_message = str("There are " + str(agg_results) + " total " + selected_dimension.lower() + " titles in my collection.")
            st.markdown(f"""
            ##### {display_message}
            """)
    if selected_measure == 'Completed Count':
        if selected_dimension == 'N/A - Use the whole table':
            display_message = str('I have finished reading ' + str(agg_results) + " of my books.")
            st.markdown(f"""
            ##### {display_message}
            """)
        else:
            display_message = str('I have finished reading ' + str(agg_results) + " of the " + selected_dimension.lower() + \
                                " titles in my collection.")
            st.markdown(f"""
            ##### {display_message}
            """)
    elif selected_measure == 'Pages':
        if selected_title is None:
            if selected_dimension == 'N/A - Use the whole table':
                display_message = str('The ' + selected_agg + ' of the pages for my whole collection is ' + str(agg_results) + ".")
                st.markdown(f"""
            ##### {display_message}
            """)
            else:
                display_message = str('The ' + selected_agg.lower() + ' of the pages of the ' + selected_dimension.lower() +\
                                    ' books in my collection is ' + str(agg_results) + ".")
                st.markdown(f"""
            ##### {display_message}
            """)
        else:
            if selected_dimension == 'N/A - Use the whole table':
                display_aggregate_message = str('The ' + selected_agg.lower() + ' pages for a book in my collection is ' + \
                        str(agg_results) + ".")
                display_title_message = str('The book with the ' + selected_agg.lower() + ' number of pages is "' + \
                        selected_title + '."')
                st.markdown(f"""
            ##### {display_aggregate_message}
            """)
                st.markdown(f"""
            ##### {display_title_message}
            """)
                if st.button("View title entry:"):
                    filtered_dataframe = dataframe[dataframe['title'] == selected_title]
                    st.write(filtered_dataframe)
                    if st.button("Clear"):
                        st.button("View title entry:") == False
                # formatted_title = selected_title.replace(' ', '+')
                # url = f"https://bookshop.org/search?keywords={formatted_title}"
                # st.write(f'<a href="{url}" target="_blank">Buy the book</a>', unsafe_allow_html=True)
            else:
                display_aggregate_message = str('The ' + selected_agg.lower() + ' pages for a ' + selected_dimension.lower() + ' title in my collection is ' + \
                        str(agg_results) + ".")
                display_title_message = str('The '+ selected_dimension.lower() + ' title with the ' + selected_agg.lower() + ' number of pages is "' + \
                        selected_title + '."')
                st.markdown(f"""
            ##### {display_aggregate_message}
            """)
                st.markdown(f"""
            ##### {display_title_message}
            """)
                if st.button("View title entry:"):
                    filtered_dataframe = dataframe[dataframe['title'] == selected_title]
                    st.write(filtered_dataframe)
                    if st.button("Clear"):
                        st.button("View title entry:") == False
                # formatted_title = selected_title.replace(' ', '+')
                # url = f"https://bookshop.org/search?keywords={formatted_title}"
                # st.write(f'<a href="{url}" target="_blank">Buy the book</a>', unsafe_allow_html=True)
    elif selected_measure == 'Year':
        if selected_title is None:
            if selected_dimension == 'N/A - Use the whole table':
                display_message = str('The ' + selected_agg.lower() + ' for a title in my collection is ' + str(agg_results) + ".")
                st.markdown(f"""
            ##### {display_message}
            """)
            else:
                display_message = str('The ' + selected_agg.lower() + ' for the ' + selected_dimension.lower() +\
                                    ' titles in my collection is ' + str(agg_results) + ".")
                st.markdown(f"""
            ##### {display_message}
            """)
        else:
            if selected_dimension == 'N/A - Use the whole table':
                display_aggregate_message = str('The ' + selected_agg.lower() + ' published book in my collection is ' + \
                        str(agg_results) + ".")
                display_title_message = str('The book with the ' + selected_agg.lower() + ' year of publication is "' + \
                        selected_title + '."')
                st.markdown(f"""
            ##### {display_aggregate_message}
            """)
                st.markdown(f"""
            ##### {display_title_message}
            """)
                if st.button("View title entry:"):
                    filtered_dataframe = dataframe[dataframe['title'] == selected_title]
                    st.write(filtered_dataframe)
                    if st.button("Clear"):
                        st.button("View title entry:") == False
                # formatted_title = selected_title.replace(' ', '+')
                # url = f"https://bookshop.org/search?keywords={formatted_title}"
                # st.write(f'<a href="{url}" target="_blank">Buy the book</a>', unsafe_allow_html=True)
            else:
                display_aggregate_message = str('The ' + selected_agg.lower() + ' published ' + selected_dimension.lower() + ' book in my collection is ' + \
                            str(agg_results) + ".")
                display_title_message = str('The ' + selected_dimension.lower() + ' book with the ' + selected_agg.lower() + ' year of publication is "' + \
                        selected_title + '."')
                st.markdown(f"""
            ##### {display_aggregate_message}
            """)
                st.markdown(f"""
            ##### {display_title_message}
            """)
                if st.button("View title entry:"):
                    filtered_dataframe = dataframe[dataframe['title'] == selected_title]
                    st.write(filtered_dataframe)
                    if st.button("Clear"):
                        st.button("View title entry:") == False
                # formatted_title = selected_title.replace(' ', '+')
                # url = f"https://bookshop.org/search?keywords={formatted_title}"
                # st.write(f'<a href="{url}" target="_blank">Buy the book</a>', unsafe_allow_html=True)



main()






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

