#!/usr/bin/env python3

import json
import lyricsgenius
import markovify

GENIUS_CLIENT_TOKEN = ''
file_names = []
artist_names = []
output_file = 'merged_lyrics.txt'
limit = 35

genius = lyricsgenius.Genius(GENIUS_CLIENT_TOKEN)
genius.verbose = True # Turn off status messages
genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
genius.skip_non_songs = True # Include hits thought to be non-songs (e.g. track lists)
genius.excluded_terms = [
    "Remix", "Live", "Unplugged", "Demo", "Bonus", 
    "Remastered", "Promo", "Version"
    ] # Exclude songs with these words in their title

def scrape_lyrics(artist_names):
    for artist in artist_names:
        artist_lyrics = genius.search_artist(artist, max_songs=limit)
        artist_lyrics.save_lyrics()

def merge_json_files(file_names):
    all_lyrics = ''

    for file_name in file_names:
        with open(file_name, 'r') as file_cont:
            json_lyrics = json.load(file_cont)
            for song in json_lyrics['songs']:
                all_lyrics += song['lyrics']

    with open(output_file, 'w') as f:
        f.write(all_lyrics)

def generate_from_jsons(file_names):
    all_lyrics = ''

    for file_name in file_names:
        with open(file_name, 'r') as file_cont:
            json_lyrics = json.load(file_cont)
            for song in json_lyrics['songs']:
                all_lyrics += song['lyrics']

    text_model = markovify.Text(all_lyrics)

    for _ in range(10):
        generated_sentence = text_model.make_short_sentence(140)
        if (generated_sentence is not None):
            print(generated_sentence)

def generate_from_txt(file_name):
    with open(file_name) as f:
        file_content = f.read()

    text_model = markovify.Text(file_content)

    for _ in range(10):
        generated_sentence = text_model.make_sentence()
        if (generated_sentence is not None):
            print(generated_sentence)
