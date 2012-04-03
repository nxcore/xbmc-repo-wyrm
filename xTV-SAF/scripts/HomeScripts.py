# HomeScripts script by Wyrm (xTV-SAF) #
# Prompt user for name of script and output skin strings #
# containing required info to run script from the home screen #

# main import's
import xbmc,xbmcgui
import os,sys

ScriptDir = 'special://xbmc/scripts'

class Main:

	# Get skin string name
	SkinStringName = string.replace(str(sys.argv[1:]),"'","")
	SkinStringName = string.replace(SkinStringName,"[","")
	SkinStringName = string.replace(SkinStringName,"]","")

	# Get the directory contents and put them in **ScriptList**
	ScriptList = os.listdir(SCRIPTDIR)
	
	# Prompt User for script name
	dialog = xbmcgui.Dialog()
	Listnum = dialog.select('Choose a Script', ScriptList)

	try:
		ScriptName = ScriptList [Listnum]
		
	except IndexError:
		sys.exit(2)
	else:		
		ScriptLocation = os.path.join(ScriptDir, ScriptName)
		ScriptIcon = os.path.join(ScriptLocation, 'default.tbn')
	
		# Write Script name and location to skin variables
		xbmc.executebuiltin("XBMC.Skin.SetString(" + SkinStringName + "-scriptloc," + ScriptLocation + ")")
		xbmc.executebuiltin("XBMC.Skin.SetString(" + SkinStringName + "-scripticon," + ScriptIcon + ")")
		xbmc.executebuiltin("XBMC.Skin.SetString(" + SkinStringName + "-scriptname," + ScriptName + ")")

if ( __name__ == "__main__" ):
    Main()
