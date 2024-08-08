import pandas as pd
from difflib import SequenceMatcher
from itertools import combinations

# Load the CSV file
file_path = 'supabase_ofuztpchpdrujpuzeqrm_Venues Table (1).csv'  # Use relative path
venues_df = pd.read_csv(file_path)

# Normalize names to lower case for comparison
venues_df['name_normalized'] = venues_df['name'].str.lower()
venues_df['city_normalized'] = venues_df['city'].str.lower()

# Create a list to store potential duplicates with their similarity scores
potential_duplicates = []

# Group by city and compare venues within each city group
grouped = venues_df.groupby('city_normalized')

for city, group in grouped:
    # Generate all possible pairs within the city group
    for (i, venue1), (j, venue2) in combinations(group.iterrows(), 2):
        similarity_score = SequenceMatcher(None, venue1['name_normalized'], venue2['name_normalized']).ratio()
        if similarity_score > 0.7:  # Lower the threshold to 0.7
            potential_duplicates.append({
                'id1': venue1['id'], 'name1': venue1['name'], 'city1': venue1['city'],
                'address1': venue1['address'], 'latitude1': venue1['latitude'], 'longitude1': venue1['longitude'],
                'future_event_count1': venue1['future_event_count'], 'future_session_count1': venue1['future_session_count'],
                'id2': venue2['id'], 'name2': venue2['name'], 'city2': venue2['city'],
                'address2': venue2['address'], 'latitude2': venue2['latitude'], 'longitude2': venue2['longitude'],
                'future_event_count2': venue2['future_event_count'], 'future_session_count2': venue2['future_session_count'],
                'similarity_score': similarity_score
            })

# Convert potential duplicates to DataFrame
potential_duplicates_df = pd.DataFrame(potential_duplicates)
potential_duplicates_df.sort_values(by='similarity_score', ascending=False, inplace=True)

# Filter by event/session counts to prioritize venues with future events/sessions
potential_duplicates_df['total_event_session_count1'] = potential_duplicates_df['future_event_count1'] + potential_duplicates_df['future_session_count1']
potential_duplicates_df['total_event_session_count2'] = potential_duplicates_df['future_event_count2'] + potential_duplicates_df['future_session_count2']
potential_duplicates_df = potential_duplicates_df[(potential_duplicates_df['total_event_session_count1'] > 0) | (potential_duplicates_df['total_event_session_count2'] > 0)]

# Display the DataFrame
print(potential_duplicates_df)

# Optionally, save the DataFrame to a CSV file
potential_duplicates_df.to_csv('potential_duplicate_venues.csv', index=False)
