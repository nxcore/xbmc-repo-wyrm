# HomePlugins script by Wyrm (xTV-SAF) #
# Prompt user for name of playlist and output skin strings #
# containing required info to run playlist from the home screen #

# main import's
import xbmc,xbmcgui
import fileinput,os,sys,re,string

PLAYLISTDIR = 'special://skin/extras/playlists'

def getplaylisttype():
	# Get the directory contents and put them in **MainPlaylistList**
	MainPlaylistList = os.listdir(PLAYLISTDIR)
	
	# Prompt User for playlist type
	dialog = xbmcgui.Dialog()
	Listnum = dialog.select(xbmc.getLocalizedString(20006), MainPlaylistList)

	try:
		PlaylistTYPE = MainPlaylistList [Listnum]
		
	except IndexError:
		sys.exit(2)
	else:
		return PlaylistTYPE

def getplaylistname(Location):
	# Get the directory contents and put them in **PlaylistList**
	PlaylistList = os.listdir(Location)
	
	# Prompt User for playlist name
	dialog = xbmcgui.Dialog()
	Listnum = dialog.select(xbmc.getLocalizedString(656), PlaylistList)

	try:
		PlaylistNAME = PlaylistList [Listnum]
		
	except IndexError:
		sys.exit(2)
	else:
		return PlaylistNAME
		
def getplaylisticon(ListType):

		if 'music' in ListType:
			IconName = 'DefaultAudio.png'
			return IconName

		else:
			IconName = 'DefaultMovies.png'
			return IconName
			
def main():
	SkinStringName = string.replace(str(sys.argv[1:]),"'","")
	SkinStringName = string.replace(SkinStringName,"[","")
	SkinStringName = string.replace(SkinStringName,"]","")

	PlaylistType = getplaylisttype()
	PlaylistLOCATION = os.path.join(PLAYLISTDIR, PlaylistType)
	Playlist = getplaylistname(PlaylistLOCATION)
	
	PlaylistLabel = string.replace(Playlist,".xsp","")

	PlaylistIcon = getplaylisticon(PlaylistType)

	# Write out Skin strings with plugin info
	xbmc.executebuiltin("XBMC.Skin.SetString(" + SkinStringName + "-playlistloc," + Playlist + ")")
	xbmc.executebuiltin("XBMC.Skin.SetString(" + SkinStringName + "-playlistlabel," + PlaylistLabel + ")")
	xbmc.executebuiltin("XBMC.Skin.SetString(" + SkinStringName + "-playlisticon," + PlaylistIcon + ")")
	xbmc.executebuiltin("XBMC.Skin.SetString(" + SkinStringName + "-playlisttype," + PlaylistType + ")")

if __name__ == '__main__':
	main()	

