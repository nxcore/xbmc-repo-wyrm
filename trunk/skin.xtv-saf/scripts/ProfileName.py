import xbmc,xbmcgui
import fileinput,os,sys,re,string

PROFILESFILE = 'special://userdata/profiles.xml'
SKINHOME = 'special://skin'
READMODE = 'r'
xml = []

def getprofilename(xml):
	# process all profiles in XML for profile names

	try:

		f = open(PROFILESFILE , READMODE)
		s = f.read()
		f.close()
		ls = s.split("\n") # This means each new line will be loaded into it's own array.
		
		for l in ls:
		
			l = string.lstrip(l)
			
			if '<name>' in l:
				l = string.replace(l, '<name>' , '')
				l = string.replace(l, '</name>' , '')
				xml.append(l)
				NumberProfiles = NumberProfiles + 1
				print ("Number of profiles Thus far" , NumberProfiles)
				continue
			
	except:
		print str( sys.exc_info()[ 1 ] )
	
def selectprofile(xml):	
	# Prompt User for profile name

	Listnum = xbmcgui.Dialog().select(xbmc.getLocalizedString(31440) ,xml)
	print (xbmc.getLocalizedString(31440))
	return Listnum
	
def main():

	try:
		getprofilename(xml)
		Listnum = selectprofile(xml)
		xbmc.executebuiltin("XBMC.Skin.SetString(home-familypname," + xml[Listnum] + ")")
	except IndexError:
		sys.exit(2)

if __name__ == '__main__':
	main()	
