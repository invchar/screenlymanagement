import requests
import sys
import os

HOST = "https://api.screenlyapp.com"
API_ROOT = "/api/v3"
API_KEY = os.getenv('API_KEY')

session = requests.Session()

session.headers["Authorization"] = "Token {}".format(API_KEY)

def enablePlaylist(playlistID, enabled):
	r = session.patch((HOST + API_ROOT + "/playlists/{}/".format(playlistID)),({"is_enabled":enabled}))

def getPlaylistIds():
	r = session.get((HOST + API_ROOT + "/playlists"))
	playlists = r.json()
	playlistIds = []
	for playlist in playlists:
		playlistIds.append(playlist["id"])
	return playlistIds

def getPlaylistAssetIds(playlistID):
	r = session.get((HOST + API_ROOT + "/playlists/{}".format(playlistID)))
	playlist = r.json()
	assets = playlist["assets"]
	assetIds = []
	for asset in assets:
		assetIds.append(asset["_id"])
	return assetIds

#def replaceAsset(oldAssetId, newAssetId):
#	playlistIds = getPlaylistIds()
#	masterList = {}
#	for playlistId in playlistIds:
#		masterList.update({playlistId:getPlaylistAssetIds(playlistId)})
#	for playlistId, assets in masterList.items():
#		if oldAssetId in assets:

