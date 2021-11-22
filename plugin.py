#!/usr/bin/env python3


"""Extracting IDs from document"""
def idExtractor(channelID, document):
    for key in document:
        try:
            if document[key][0] == channelID:
                return key, document[key][1]
        except TypeError:
            continue
    return

# def findChannelID(channelID, document):


