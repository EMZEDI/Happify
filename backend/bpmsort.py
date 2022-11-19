import numpy as np
import pandas as pd
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import cred
from spotipy.oauth2 import SpotifyOAuth



def playlist_tracks_IDList_generator(playlist_id, spotify: spotipy.Spotify):
    """
    Gets a playlist ID & returns a list of all tracks IDs
    :param playlist_id: int
    :param spotify: Spotify
    :return: tracks_ID_List: list
    """
    # counter of the loop
    i: int = 0
    # Track ID list
    iD_list: list = []
    item_list = []
    curr = []
    # 100 by 100 add songs to the list
    offset = 0

    while True:
        # first iteration
        curr = spotify.playlist_items(playlist_id=playlist_id, offset=offset)['items']
        if len(curr) == 0:
            break
        item_list += curr
        offset += 100
    # print(curr)

    # create the final ID list
    while True:

        try:
            iD_list.append(item_list[i]['track']['id'])
            i += 1
        except:
            break
    
    return iD_list

# get the current mood of the user and add a song to the queue 
def create_feature_dataset(all_playlists_IDList: list, spotify: spotipy.Spotify):
    """
    read:
    :param all_playlists_IDList: List of all IDs for the total playlists
    :param spotify: Spotify
    :return: dataframe of all songs and their features collected from the whole input
    """
    final_df = pd.DataFrame({})
    # iterate thru each playlist and create rows of the final dataset and add to the dataframe to be returned
    for playlist_ID in all_playlists_IDList:

        # we have the playlist and have to create the list of tracks IDs of that specific playlist
        tracksIDs: list = playlist_tracks_IDList_generator(playlist_ID, spotify)
        # iterate thru the list of track IDs and generate each feature

        for trackID in tracksIDs:
            try:
                feat_dict = spotify.audio_features(trackID)
                coln = pd.DataFrame(feat_dict)
                coln.drop('analysis_url', axis=1, inplace=True)
                coln.drop('track_href', axis=1, inplace=True)
                coln.drop('uri', axis=1, inplace=True)
                coln.drop('type', axis=1, inplace=True)
                final_df = pd.concat([final_df, coln], ignore_index=True)
            # for songs that don't work
            except:
                continue

    final_df.set_index('id', inplace=True)
    # print(final_df)
    # remove duplicates from the dataframe
    final_df.drop_duplicates(keep='last', inplace=True)

    final_df['id'] = final_df.index
    return final_df

def get_song_features(songid, spotify):
    single_features = pd.Series(spotify.audio_features(songid)[0])
    return single_features

# THE API functions are working. 
def mood_changer(current_songid, pl1, pl2, pl3, pl4, longterm_emotion: int, spot):
    """
    A function designed to find the best choice to make the user happier
    """
    
    current_features = get_song_features(current_songid, spot)
    item = [pl1, pl2, pl3, pl4][longterm_emotion]
    df = create_feature_dataset([item], spot)
    df = df[df['id'] != current_songid] # take care of repetition 
    # sort the dataframe based on the each mood
    # if the mood is overall good dont change anything
    if longterm_emotion == 1:
        # add more dance songs 
        for feature in ["danceability", "energy", "liveness", "loudness"]:
            df.sort_values(by=[feature], inplace=True)
            # print(df)
            if max(df[feature]) < current_features[feature]:
                continue
            else:
                try:
                    # print(df[feature])
                    # print(current_features[feature])
                    next_song = df[df[feature] > current_features[feature]]
                    break
                except:
                    continue

    elif longterm_emotion == 2:
        for feature in ["energy", "liveness", "danceability", "loudness"]:
            df.sort_values(by=[feature], inplace=True)
            # print(df)
            if max(df[feature]) < current_features[feature]:
                continue
            else:
                try:
                    # print(df[feature])
                    # print(current_features[feature])
                    next_song = df[df[feature] > current_features[feature]]
                    break
                except:
                    continue

    elif longterm_emotion == 3:
        for feature in ["energy", "loudness", "danceability", "loudness"]:
            df.sort_values(by=[feature], inplace=True)
            if max(df[feature]) < current_features[feature]:
                continue
            else:
                try:
                    next_song = df[df[feature] > current_features[feature]]
                    break
                except:
                    continue

    return next_song.iloc[0,:].id


if __name__ == "__main__":
    # scope = "user-read-recently-played user-read-currently-playing ugc-image-upload user-read-private user-library-modify playlist-modify-public user-library-read playlist-read-private playlist-read-collaborative app-remote-control streaming"
    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret= cred.client_secret, redirect_uri=cred.redirect_url, scope=scope))
    ID = ""

    secret = ""

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=ID, client_secret=secret))

    current_songid = ""
    pl1= ""
    pl2= ""
    pl3= ""
    pl4= ""

    print(mood_changer(current_songid, pl1, pl2, pl3, pl4, 2, sp))

    # new_song = mood_changer(current_songid, pl1, pl2, pl3, pl4, 2, sp)