#py -m streamlit run dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px


def dashboard(dataframe):
    st.title("Adam's Books Dashboard")
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


        #This actually filters the dataframe according to the selections
        filtered_dataframe = genre_filterer(filtered_dataframe, selected_genre)
        filtered_dataframe = decade_filterer(filtered_dataframe, selected_decade)


    with col[1]: 
        st.markdown('Select a Subset')
        a, b, c, d, e, f = st.columns(6)
        g, h = st.columns(2)
        a.metric('Total Books', filtered_dataframe['title'].count(), border=True)
        b.metric('Books Completed', filtered_dataframe[filtered_dataframe['read_by_adam'] == 2]['read_by_adam'].count(), border=True)
        c.metric('Total Page Count', filtered_dataframe['page_count'].sum(), border=True)
        d.metric('Pages Read', filtered_dataframe[filtered_dataframe['read_by_adam'] == 2]['page_count'].sum(), border=True)

        median_pages = str(filtered_dataframe['page_count'].median())
        median_pages = median_pages[:-2]
        e.metric('Median Page Count', median_pages, border=True)

        average_year = str(filtered_dataframe['original_copyright_year'].mean().round(decimals=0))
        average_year = average_year[:-2]
        f.metric('Avg Publication Year', average_year, border=True)

    
        # Pie chart, part un
        #This creates a dataframe of what was filtered out by the slicer choices
        
        remainder_dataframe = pd.concat([dataframe, filtered_dataframe]).drop_duplicates(keep=False)

        data = {"Names": [" Selection", " Remaining Collection",],\
                "Count" : [(filtered_dataframe['title']).count(),\
                            (remainder_dataframe['title']).count()]}
        pie_chart_dataframe = pd.DataFrame(data)
        pie_chart = px.pie(pie_chart_dataframe, values = "Count", names = "Names", color = "Names",\
                            color_discrete_map={' Selection':'blue',' Remaining Collection':'lightblue'})
        pie_chart.update_layout(title='% of Total Collection', showlegend=False)
        pie_chart.update_traces(textposition='inside', textinfo='percent+label')
        g.plotly_chart(pie_chart)


        #bar chart
        filtered_dataframe.rename(columns={'original_copyright_year': 'Year'}, inplace=True)
        if selected_decade not in ('1800-1899', 'Pre-1800'):
            filtered_dataframe['Year'] = filtered_dataframe['Year'].astype(int)
            filtered_dataframe = filtered_dataframe.loc[filtered_dataframe["Year"] >= 1900]
            filtered_dataframe['Year'] = filtered_dataframe['Year'].astype(str)
            bar_chart = px.bar(filtered_dataframe, x='Year')
            bar_chart.update_layout(title='Book Count by Publication Year', showlegend=False)
            h.plotly_chart(bar_chart)
        else:
            filtered_dataframe['Year'] = filtered_dataframe['Year'].astype(str)
            bar_chart = px.bar(filtered_dataframe, x='Year')
            bar_chart.update_layout(title='Book Count by Publication Year', showlegend=False)
            h.plotly_chart(bar_chart)

        # #Multi Author chart
        # author_counts = filtered_dataframe['author'].value_counts()
        # filtered_dataframe['author count'] = filtered_dataframe['author'].map(author_counts)
        # multi_authors = author_counts[author_counts > 1].index
        # multi_authors_df = filtered_dataframe[filtered_dataframe['author'].isin(multi_authors)]
        # multi_authors_grouped_df = multi_authors_df.groupby('author').agg({'title':['count']})
        # f.markdown('#### Most Popular Authors')
        # f.dataframe(multi_authors_grouped_df, height = 240)
