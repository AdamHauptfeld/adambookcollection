import streamlit as st
from annotated_text import annotated_text as annotate
import pandas as pd
from streamlit_option_menu import option_menu

def dataset_viewer(dataframe):
     
    st.title("Adam's Book Collection")
    col = st.columns((1.5,6.5), gap='medium')

    def genre_filterer(filtered_dataframe, selected_genre):
        if selected_genre == 'All Genres':
            pass
        else:
            filtered_dataframe = filtered_dataframe[dataframe['genre'].str.contains(rf'\b{selected_genre}\b', na=False)]
        return filtered_dataframe

    def decade_filterer(filtered_dataframe, selected_decade):
        if selected_decade == 'All Decades':
            pass
        elif selected_decade == '2020s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(2020, 2029)]
        elif selected_decade == '2010s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(2010, 2019)]
        elif selected_decade == '2000s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(2000, 2009)]
        elif selected_decade == '1990s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(1990, 1999)]
        elif selected_decade == '1980s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(1980, 1989)]
        elif selected_decade == '1970s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(1970, 1979)]
        elif selected_decade == '1960s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(1960, 1969)]
        elif selected_decade == '1950s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(1950, 1959)]
        elif selected_decade == '1940s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(1940, 1949)]
        elif selected_decade == '1930s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(1930, 1939)]
        elif selected_decade == '1920s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(1920, 1929)]
        elif selected_decade == '1910s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(1910, 1919)]
        elif selected_decade == '1900s':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(1900, 1909)]
        elif selected_decade == '1800-1899':
            filtered_dataframe = filtered_dataframe[filtered_dataframe['original_copyright_year'].between(1800, 1899)]
        elif selected_decade == 'Pre-1800':
            filtered_dataframe = filtered_dataframe[(filtered_dataframe['original_copyright_year'] <= 1809)]
        return filtered_dataframe


    #This is the slicer column
    with col[0]: 
        dimensions = ['N/A - Use the whole table', 'Fiction', 'Non-fiction',  'Finished', 'Unfinished', 'Favorites', 'Hardcover', 'Softcover']
        selected_dimension = st.selectbox("Select a filter:", dimensions)
        if selected_dimension == 'N/A - Use the whole table':
            filtered_dataframe = dataframe
        elif selected_dimension == 'Fiction':
            filtered_dataframe = dataframe[dataframe['fiction'] == 1]
        elif selected_dimension == 'Non-fiction':
            filtered_dataframe = dataframe[dataframe['fiction'] == 0]
        elif selected_dimension == 'Favorites':
            filtered_dataframe = dataframe[dataframe['all_time_fave'] == 1]
        elif selected_dimension == 'Finished':
            filtered_dataframe = dataframe[dataframe['read_by_adam'] == 2]
        elif selected_dimension == 'Unfinished':
            filtered_dataframe = dataframe[dataframe['read_by_adam'] != 2]
        elif selected_dimension == 'Hardcover':
            filtered_dataframe = dataframe[dataframe['hardcover'] == 1]
        elif selected_dimension == 'Softcover':
            filtered_dataframe = dataframe[dataframe['hardcover'] == 0]

        #Filter dataframe by genre
        #this gets me a list of all genres, including those combined with the forward slash delimiter
        genre_lists = filtered_dataframe['genre'].str.split('/')
        all_genres = [genre.strip() for genres in genre_lists for genre in genres]
        unique_genres = list(set(all_genres))
        unique_genres.sort()
        unique_genres.insert(0, 'All Genres')
        selected_genre = st.selectbox("Select a genre: ", unique_genres)

        #Filter dataframe by decade
        decades = ['All Decades', '2020s', '2010s', '2000s', '1990s', '1980s', '1970s', '1960s', '1950s', '1940s', '1930s', '1920s',\
                '1910s', '1900s', '1800-1899', 'Pre-1800']
        selected_decade = st.selectbox("Select a decade: ", decades)

        #For choosing simple or full table
        full_table = st.checkbox('Check for Full Table')

        with st.expander('Table Documentation'):
            table_documentation = '''
            title - Main title of book

            subtitle - Subtitle of book

            author - First listed author of book written as it appears on cover (probably first name last name)

            other authors - Any authors other than the first listed author, possibly author of foreword or a translator

            publisher - Self-explanatory

            fiction - 1 for fiction, 0 for non-fiction

            genre - Pretty general ("Science" rather than "Biology", "Science Fiction" rather than "Hard Sci-Fi", can use '/' delimiter

            keywords - Strings between double quotes to prevent commas from being interpreted as delimiters

            page_count - This is the last numbered page in the book, possibly on index or appendix page

            original_publication_year - Year of original copyright

            latest_listed_year - Last year included in the copywrite page, possibly null

            read_by_adam - 0 for not read, 1 for partially read, 2 for finishedL

            read_by_wife - 0 for not read, 1 for partially read, 2 for finished

            hardcover - 0 for softcover, 1 for hardcover

            notes - Varies
                     '''
            st.write(table_documentation)




        #This actually filters the dataframe according to the selections
        filtered_dataframe = genre_filterer(filtered_dataframe, selected_genre)
        filtered_dataframe = decade_filterer(filtered_dataframe, selected_decade)

   
    #This displays the dataset
    with col[1]:
        if not full_table:
            filtered_dataframe['original_copyright_year'] = filtered_dataframe['original_copyright_year'].astype(str).str.replace(",", "")
            filtered_dataframe.rename(columns={'original_copyright_year': 'year'}, inplace=True)
            def clean_year(x):
                if pd.notnull(x):
                    x = int(x)
                    return str(x).replace(',', '')
            filtered_dataframe['latest_listed_year'] = filtered_dataframe['latest_listed_year'].apply(clean_year)

            #This displays the simplified table and also stores the row of any selection the user makes.
            selected_row = st.dataframe(filtered_dataframe[['title', 'author', 'genre', 'year', 'keywords']],
            hide_index=True,
            on_select='rerun',
            selection_mode='single-row'
            ).selection
        else:
            filtered_dataframe['original_copyright_year'] = filtered_dataframe['original_copyright_year'].astype(str).str.replace(",", "")
            filtered_dataframe.rename(columns={'original_copyright_year': 'year'}, inplace=True)
            def clean_year(x):
                if pd.notnull(x):
                    x = int(x)
                    return str(x).replace(',', '')
            filtered_dataframe['latest_listed_year'] = filtered_dataframe['latest_listed_year'].apply(clean_year)

            #This displays the simplified table and also stores the row of any selection the user makes.
            selected_row = st.dataframe(filtered_dataframe,
            hide_index=True,
            on_select='rerun',
            selection_mode='single-row'
            ).selection
        
        




    
    # #This handles displaying a selected title and generate a link to buy it.
    # if selected_row and len(selected_row['rows']) > 0:
    #     row_index = selected_row['rows'][0]
    #     just_selected_row = book_table.iloc[row_index:row_index+1]
        
    #     # Display the filtered row
    #     st.markdown("""
    #     ##### Selected Row Details
    #     """)
    #     st.write(just_selected_row)

    #     #Generate purchase link
    #     selected_title = just_selected_row['title'].iloc[0]
    #     selected_author = just_selected_row['author'].iloc[0]
    #     formatted_title = selected_title.replace(' ', '+')
    #     formatted_author = selected_author.replace(' ', '+')
    #     url = f"https://bookshop.org/search?keywords={formatted_title}+{formatted_author}"
    #     st.write(f'<a href="{url}" target="_blank">Buy {selected_title} by {selected_author} on Bookshop.org</a>', unsafe_allow_html=True)
    #     annotate('The author is ', (selected_author, ''), ".")