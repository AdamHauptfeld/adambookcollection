import streamlit as st
import pandas as pd

def table_dimension_filterer(dataframe):
    dimensions = ['Genre', 'Fiction', 'Non-fiction', 'Publisher', 'Favorites',  'Finished (by Adam)', 'N/A - Use the whole table']
    
    #Create dataframe filtered by dimension choice.
    selected_dimension = st.selectbox("Select a dimension to filter by:", dimensions, index=4)
    if selected_dimension == 'Genre':
        #this gets me a list of all genres, including those combined with the forward slash delimiter
        genre_lists = dataframe['genre'].str.split('/')
        all_genres = [genre.strip() for genres in genre_lists for genre in genres]
        unique_genres = list(set(all_genres))
        unique_genres.sort()
        selected_genre = st.selectbox("Select a genre: ", unique_genres)
        filtered_dataframe = dataframe[dataframe['genre'].str.contains(rf'\b{selected_genre}\b', na=False)]
        selected_dimension = selected_genre
    elif selected_dimension == 'Fiction':
        filtered_dataframe = dataframe[dataframe['fiction'] == 1]
    elif selected_dimension == 'Non-fiction':
        filtered_dataframe = dataframe[dataframe['fiction'] == 0]
    elif selected_dimension == 'Publisher':
        publisher_list = dataframe['publisher'].tolist()
        publisher_list = list(set(publisher_list))
        publisher_list.sort()
        selected_publisher = st.selectbox("Select a publisher: ", publisher_list)
        filtered_dataframe = dataframe[dataframe['publisher'] == selected_publisher]
        selected_dimension = selected_publisher
    elif selected_dimension == 'Favorites':
        filtered_dataframe = dataframe[dataframe['all_time_fave'] == 1]
    elif selected_dimension == 'Finished (by Adam)':
        filtered_dataframe = dataframe[dataframe['read_by_adam'] == 2]
    elif selected_dimension == 'N/A - Use the whole table':
        filtered_dataframe = dataframe

    return filtered_dataframe, selected_dimension


def table_aggregator(dataframe):
    measures = ['Pages', 'Year', 'Titlecount', 'Completed Count']
    selected_measure = st.selectbox("Select a measure to aggregate:", measures, index=2)
    
    if selected_measure == 'Titlecount':
        agg_results = dataframe['title'].count()
        selected_agg = None
        selected_title = None
        return agg_results, selected_measure, selected_agg, selected_title
    
    elif selected_measure == 'Pages':
        page_aggregations = ['Sum', 'Average', 'Minimum', 'Maximum', 'Standard deviation']
        page_aggregations_dict = {'Sum':dataframe['page_count'].sum(),\
                                'Average':dataframe['page_count'].mean().round(2),\
                                'Minimum':dataframe['page_count'].min(),\
                                'Maximum':dataframe['page_count'].max(),\
                                'Standard deviation':dataframe['page_count'].std().round(2)}
        selected_agg = st.selectbox("Select an aggregation: ", page_aggregations)
        agg_results = page_aggregations_dict[selected_agg]
        if selected_agg in ['Minimum', 'Maximum']:
            selected_title = dataframe[dataframe['page_count'] == agg_results]['title'].iloc[0]
            return agg_results, selected_measure, selected_agg, selected_title
        else:
            selected_title = None
            return agg_results, selected_measure, selected_agg, selected_title
    
    elif selected_measure == 'Year':
        year_aggregations = ['Earliest', 'Latest', 'Median year', 'Mode year']
        year_aggregation_dict = {'Earliest':dataframe['original_copyright_year'].min(),\
                                'Latest':dataframe['original_copyright_year'].max(),\
                                'Median year':dataframe['original_copyright_year'].median(),\
                                'Mode year':dataframe['original_copyright_year'].mode().iloc[0]}
        selected_agg = st.selectbox("Select an aggregation: ", year_aggregations)
        agg_results = year_aggregation_dict[selected_agg]
        if selected_agg in ['Earliest', 'Latest']:
            selected_title = dataframe[dataframe['original_copyright_year'] == agg_results]['title'].iloc[0]
            return agg_results, selected_measure, selected_agg, selected_title
        else:
            selected_title = None
            return agg_results, selected_measure, selected_agg, selected_title
        
    elif selected_measure == 'Completed Count':
        completed_table = dataframe[dataframe['read_by_adam']==2]
        agg_results = completed_table['title'].count()
        selected_agg = None
        selected_title = None
        return agg_results, selected_measure, selected_agg, selected_title
