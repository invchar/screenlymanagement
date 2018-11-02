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
parser.add_argument('--action', choices=['enablePlaylists','removeAsset','replaceAsset'])
parser.add_argument('--playlistIds')
parser.add_argument('--assetId')
parser.add_argument('--oldAssetId')
parser.add_argument('--newAssetId')
parser.add_argument('--duration')
args = parser.parse_args()

def enablePlaylists(playlistIds, enabled):
	if ('ALL' in playlistIds):
		playlistIds = getPlaylistIds()
	for playlistId in playlistIds:
		session.patch((HOST + API_ROOT + "/playlists/{}/".format(playlistId)),({"is_enabled":enabled}))
	return 0

def getPlaylistIds():
	r = session.get('{}/{}/playlists/'.format(HOST,API_ROOT))
	playlists = r.json()
	playlistIds = []
	for playlist in playlists:
		playlistIds.append(playlist["id"])
	return playlistIds

def getPlaylistAssetIds(playlistId):
	r = session.get((HOST + API_ROOT + "/playlists/{}".format(playlistId)))
	playlist = r.json()
	assets = playlist["assets"]
	assetIds = []
	for asset in assets:
		assetIds.append(asset["_id"])
	return assetIds

def getPlaylistAssets(playlistId):
	r = session.get('{}/{}/playlists/{}/'.format(HOST,API_ROOT,playlistId))
	playlist = r.json()
	return playlist["assets"]

def removeAsset(playlistIds,assetId):
	if ('ALL' in playlistIds):
		playlistIds = getPlaylistIds()
	for playlistId in playlistIds:
		originalAssets = getPlaylistAssets(playlistId)
		newAssets = []
		for asset in originalAssets:
			if (asset["_id"] != assetId):
				asset["id"] = asset["_id"]
				newAssets.append(asset)
		session.patch('{}/{}/playlists/{}/'.format(HOST,API_ROOT,playlistId),data = json.dumps({"assets":newAssets}))
	return 0

def replaceAsset(playlistIds,oldAssetId,newAssetId,duration):
	if ('ALL' in playlistIds):
		playlistIds = getPlaylistIds()
	for playlistId in playlistIds:
		originalAssets = getPlaylistAssets(playlistId)
		newAssets = []
		for asset in originalAssets:
			if (asset["_id"] == oldAssetId):
				newAssets.append({"id":newAssetId,"duration":duration})
			else:
				asset["id"] = asset["_id"]
				newAssets.append(asset)
		session.patch('{}/{}/playlists/{}/'.format(HOST,API_ROOT,playlistId),data = json.dumps({"assets":newAssets}))
	return 0

if (vars(args)['action']):
	if (vars(args)['action'] == 'enablePlaylists'):
		enablePlaylists(vars(args)['playlistIds'],True)
	if (vars(args)['action'] == 'removeAsset'):
		removeAsset(vars(args)['playlistIds'],vars(args)['assetId'])
	if (vars(args)['action'] == 'replaceAsset'):
		replaceAsset(vars(args)['playlistIds'],vars(args)['oldAssetId'],vars(args)['newAssetId'],vars(args)['duration'])
