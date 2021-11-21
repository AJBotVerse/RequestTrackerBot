#!/usr/bin/env python3


"""Extracting IDs from document"""
def idExtractor(channelID, document):
    for key in document:
        if document[key][0] == channelID:
            return key, document[key][1]
    return

