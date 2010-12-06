import xbmc,xbmcgui
import os,sys

SCRIPTDIR = 'special://xbmc/scripts'
SKINFILESDIR = 'special://skin/PAL'
FILEMODE = 'w'

class Main:

	# Get the directory contents and put them in **ScriptList**
	ScriptList = os.listdir(SCRIPTDIR)
	
	# Prompt User for script name
	dialog = xbmcgui.Dialog()
	Listnum = dialog.select('Choose a Script', ScriptList)

	try:
		SCRIPTNAME = ScriptList [Listnum]
		
	except IndexError:
		sys.exit(2)
	else:		
		SCRIPTLOCATION = os.path.join(SCRIPTDIR, SCRIPTNAME)
		SCRIPTICON = os.path.join(SCRIPTLOCATION, 'default.tbn')
	
		# Write Script name and location to skin variables
		xbmc.executebuiltin("XBMC.Skin.SetString(home-scriptname," + SCRIPTNAME + ")")
		xbmc.executebuiltin("XBMC.Skin.SetString(home-scriptlocation," + SCRIPTLOCATION + ")")
		print SCRIPTICON,SCRIPTLOCATION
	
	try:
		INCLUDESCRIPT = os.path.join(SKINFILESDIR, "HomeMenuScript.xml")
 		f = open(xbmc.translatePath(INCLUDESCRIPT), FILEMODE)
		
	except IOError:
		xbmcgui.Dialog().ok('could not open file ',INCLUDESCRIPT)
	else:	
		# Write out the conditional include file
		f.write('<includes>' + '\n')
		f.write('	<include name="homescreenscript">' + '\n')
		f.write('		<icon>' + SCRIPTICON + '</icon>' + '\n')
		f.write('		<thumb>' + SCRIPTICON + '</thumb>' + '\n')
		f.write('		<label>' + SCRIPTNAME + '</label>' + '\n')
		f.write('	</include>' + '\n')
		f.write('</includes>' + '\n')
			
		f.flush()
		f.close()
		del f
		
	xbmc.executebuiltin('XBMC.ReloadSkin()')

if ( __name__ == "__main__" ):
    Main()
