#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods for parsing and processing the lyrics information (and song mapping)

@author: evilaz
"""
import pandas as pd


# Load artist-song-id-mapping to dataframe
data_df = pd.read_csv('data/mxm_779k_matches.txt', sep="<SEP>", header=None, skiprows=18,
                   names=['tid','artist_name','title', 'mxm_tid', 'artist_name_mxm','title_mxm'])

# d = data_df.to_dict(orient='dict')


def parse_lyrics_text_file(filename):
    """Reads the lyrics txt files.
    The given files have the tracks already in the bag of words model.
    It returns the vocabulary with the 1000 most frequent terms as a word-index
    mapping and the song information with track ids, mxm track id and
    word frequencies of each track (bag of words).
    Args:
        filename: filename of lyrics txt file.
    Returns:
        data: list
        data_structured: dict with key track id and value dict {mxm_id, tf_data}
    """

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    data = [] #not necessary
    data_structured = {}
    # or should one of the ids be key?

    len(lines)
    # todo I don't take all lines yes..
    for line in lines:
        # every line that doesn't start with %# is a song tf representation
        if not (line.startswith(('%', '#'))):
            line = line.strip('\n')
            data.append(line)
            track_id = line.split(',')[0]
            mxm_id = line.split(',')[1]
            tf_data = line.split(',')[2:]
            data_structured[track_id] ={'mxm_id': mxm_id, 'tf_data': tf_data}
        # ignore comments
        elif line.startswith('#'):
            continue
        # keep vocabulary (as one string)
        elif line.startswith('%'):
            voc_str = line.strip('%')
            continue
        else:
            raise Exception('Unknown line')

    return data, data_structured


def read_vocabulary(filename):

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    line = lines[17].strip('\n')
    if line.startswith('%'):
        voc_str = line.strip('%')
    else:
        raise Exception('Vocabulary not found in the specific line.')

    # Create an index of vocabulary
    words = [x for x in voc_str.split(',')]
    index = [x for x in range(1, len(words) + 1)]  # +1 because the index first word index is 1
    word_index = {key: value for (key, value) in zip(words, index)}

    return words, index, word_index


def include_tf_in_df(df, test_dict, train_dict):
    """Include data term frequency for train and test data in the dataframe"""

    df['tf'] = df.apply(lambda row: train_dict[row['tid']]['tf_data']
                             if row['tid'] in train_dict.keys() else None, axis=1)
    df['tf'] = df.apply(lambda row: test_dict[row['tid']]['tf_data']
                             if row['tid'] in test_dict.keys() else None, axis=1)

    return df


def remove_items(df, test_dict, train_dict):

    train_test_ids = list(test_dict.keys()) + list(train_dict.keys())
    train_test_df = data_df[data_df['tid'].isin(train_test_ids)].copy()

    return train_test_df




# bow = line.split(',')[2:]
# [(a,b) for a in y in {x.split(':') for x in bow}]
# '869:2'.split(':')


if __name__ == '__main__':

    filename_test = 'data/mxm_dataset_test.txt'
    filename_train = 'data/mxm_dataset_train.txt'

    words, index, word_index = read_vocabulary(filename_test)
    test_data, test_data_structured = parse_lyrics_text_file(filename_test)
    train_data, train_data_structured = parse_lyrics_text_file(filename_train)

    train_test_df = remove_items(data_df, test_data_structured, train_data_structured)

    # include tf in the dataframe
    train_test_df = include_tf_in_df(train_test_df, test_data_structured, train_data_structured)

    # not quite sure...sth is lost...Not all tf have been included for some reason
    # e.g.
    # train_test_df.iloc[11] ->
    # 'TRMMMFG128F425087B' in train_data_structured.keys()
    # train_data_structured['TRMMMFG128F425087B']

    # need to reset index as well



#
# for id in train_data_structured.keys():
#     if id in data_df['tid'].values:
#         print(id)

# Include tf representation in the dataframe
# data_df['tf'] = data_df.apply(lambda row: train_data_structured[row['tid']]['tf_data'] if row['tid'] in train_data_structured.keys() else None, axis=1)
# test['a'] = test.apply(lambda row: str(row['index1']) + '_' + str(row['a'] if row['a'] else None), axis=1)


