#!/usr/bin/env python3
import requests
import sys
import os
import json
import argparse

HOST = "https://api.screenlyapp.com"
API_ROOT = "api/v3"
API_KEY = os.getenv('API_KEY')

session = requests.Session()

session.headers = {"Authorization":"Token {}".format(API_KEY),"content-type":"application/json"}

parser = argparse.ArgumentParser(description='Manage Screenly via API')
parser.add_argument('--replace')
parser.add_argument('--with')
parser.add_argument('--playlists')
parser.add_argument('--duration')
parser.add_argument('--dump')
args = parser.parse_args()

def enablePlaylists(playlistIds, enabled):
	if ('ALL' in playlistIds):
		playlistIds = getPlaylistIds()
	for playlistId in playlistIds:
		session.patch((HOST + API_ROOT + "/playlists/{}/".format(playlistId)),({"is_enabled":enabled}))
	return 0

def getPlaylists():
	r = session.get('{}/{}/playlists/'.format(HOST,API_ROOT))
	playlists = r.json()
	return playlists

def getPlaylistIds():
	playlists = getPlaylists()
	playlistIds = []
	for playlist in playlists:
		playlistIds.append(playlist["id"])
	return playlistIds

def getPlaylistAssets(playlistId):
	r = session.get('{}/{}/playlists/{}/'.format(HOST,API_ROOT,playlistId))
	playlist = r.json()
	return playlist["assets"]

def getPlaylistAssetIds(playlistId):
	assets = getPlaylistAssets(playlistId)
	assetIds = []
	for asset in assets:
		assetIds.append(asset["id"])
	return assetIds

def dumpPlaylists(path):
	if (path.endswith(".json")):
		playlists = getPlaylists()
		datafile = open(path, "w")
		data = {"playlists":[]}
		for playlist in playlists:
			assets = getPlaylistAssets(playlist['id'])
			playlist['assets'] = assets
			data["playlists"].append(playlist)
		json.dump(data,datafile,indent=2)
		return 0
	else:
		print("Specify path and file with .json extension for dump")

def removeAsset(playlistIds,assetId):
	if ('ALL' in playlistIds):
		playlistIds = getPlaylistIds()
	for playlistId in playlistIds:
		originalAssets = getPlaylistAssets(playlistId)
		newAssets = []
		for asset in originalAssets:
			if (asset["id"] != assetId):
				newAssets.append(asset)
			else:
				print("Removing asset {} from playlist {}".format(asset["id"],playlistId))
		session.patch('{}/{}/playlists/{}/'.format(HOST,API_ROOT,playlistId),data = json.dumps({"assets":newAssets}))
	return 0

def replaceAsset(playlistIds,oldAssetId,newAssetId,duration):
	if ('ALL' in playlistIds):
		playlistIds = getPlaylistIds()
	for playlistId in playlistIds:
		originalAssets = getPlaylistAssets(playlistId)
		newAssets = []
		for asset in originalAssets:
			if (asset["id"] == oldAssetId):
				print("Replacing asset {} with {} in playlist {}".format(oldAssetId,newAssetId,playlistId))
				newAssets.append({"id":newAssetId,"duration":duration})
			else:
				newAssets.append(asset)
		session.patch('{}/{}/playlists/{}/'.format(HOST,API_ROOT,playlistId),data = json.dumps({"assets":newAssets}))
	return 0

if (vars(args)['replace']):
	replaceAsset("ALL",vars(args)['replace'],vars(args)['with'],vars(args)['duration'])
if (vars(args)['dump']):
	dumpPlaylists(vars(args)['dump'])
