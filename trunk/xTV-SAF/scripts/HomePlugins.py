import xbmc,xbmcgui
import fileinput,os,sys,re,string

PluginDIR = 'special://xbmc/plugins'

def getplugintype():
	# Get the directory contents and put them in **MainPluginList**
	MainPluginList = os.listdir(PluginDIR)
	
	# Prompt User for plugin type
	dialog = xbmcgui.Dialog()
	Listnum = dialog.select(xbmc.getLocalizedString(31442), MainPluginList)

	try:
		PluginTYPE = MainPluginList [Listnum]
		
	except IndexError:
		sys.exit(2)
	else:
		return PluginTYPE

def getpluginname(Location):
	# Get the directory contents and put them in **PluginList**
	PluginList = os.listdir(Location)
	
	# Prompt User for plugin name
	dialog = xbmcgui.Dialog()
	Listnum = dialog.select(xbmc.getLocalizedString(31443), PluginList)

	try:
		PluginNAME = PluginList [Listnum]
		
	except IndexError:
		sys.exit(2)
	else:
		return PluginNAME

def getplugintypenumber(PluginType):

		if 'music' in PluginType:
			PluginTYPENum = '501'
			return PluginTYPENum

		elif 'pictures' in PluginType:
			PluginTYPENum = '2'
			return PluginTYPENum

		elif 'programs' in PluginType:
			PluginTYPENum = '1'
			return PluginTYPENum

		elif 'video' in PluginType:
			PluginTYPENum = '24'
			return PluginTYPENum

		else:
			sys.exit(2)

def main():
	SkinStringName = string.replace(str(sys.argv[1:]),"'","")
	SkinStringName = string.replace(SkinStringName,"[","")
	SkinStringName = string.replace(SkinStringName,"]","")

	PlugType = getplugintype()
	PluginLOCATION = os.path.join(PluginDIR, PlugType)
	PlugName = getpluginname(PluginLOCATION)
	PluginFolder = os.path.join(PlugType, PlugName)
	PluginWindow = getplugintypenumber(PlugType)

	xbmc.executebuiltin("XBMC.Skin.SetString(" + SkinStringName + "-pluginfolder," + PluginFolder + ")")
	xbmc.executebuiltin("XBMC.Skin.SetString(" + SkinStringName + "-pluginwindow," + PluginWindow + ")")
	xbmc.executebuiltin("XBMC.Skin.SetString(" + SkinStringName + "-pluginname," + PlugName + ")")

if __name__ == '__main__':
	main()	

