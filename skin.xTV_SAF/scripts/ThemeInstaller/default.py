#
# Imports
#
import os
import glob
import fnmatch
import zipfile
import xbmc
import xbmcgui

#
# Init
#
SKIN_PATH        = os.path.join( xbmc.translatePath("special://home/skin"), xbmc.getSkinDir() )
SKIN_THEMES_PATH = os.path.join( SKIN_PATH, "extras", "themes" ) 
SKIN_MEDIA_PATH  = os.path.join( SKIN_PATH, "media" )
SKIN_COLORS_PATH = os.path.join( SKIN_PATH, "colors" ) 

#
# Main
#
def main() :
    #
    # Get a list of extra themes (local)
    #
    themes     = []
    
    if os.path.isdir( SKIN_THEMES_PATH ) :
        for entry in os.listdir( SKIN_THEMES_PATH ) :
            if fnmatch.fnmatch(entry, "*.zip") :
                ( name, ext ) = os.path.splitext( entry )
                themes.append( name )

    #
    # No themes found...
    #
    if not themes :
        xbmcgui.Dialog().ok( xbmc.getLocalizedString(31428), xbmc.getLocalizedString(31431) )
    
    #
    # Dialog to select theme...
    #
    else :
        dialogThemes = xbmcgui.Dialog()
        index        = dialogThemes.select( xbmc.getLocalizedString(31428), themes )
        if index != -1 :
            theme   = themes[ index ]
            install_theme( SKIN_THEMES_PATH, theme )
            
#
# Install theme
#
def install_theme( themesPath, theme ) :
    try :
        # Init
        themeZip = os.path.join( themesPath, "%s.zip" % theme )
    
        # Extract theme zip...
        zip = zipfile.ZipFile (themeZip, "r")
        for zip_entry in zip.namelist() :
        
            # XML - skin/media
            if zip_entry == "%s.xml" % theme :
                outfile = open( os.path.join( SKIN_COLORS_PATH, zip_entry ), "wb" )
                outfile.write ( zip.read( zip_entry ) )
                outfile.close()
                
            # XPR - skin/media
            elif zip_entry == "%s.xpr" % theme :
                outfile = open( os.path.join( SKIN_MEDIA_PATH, zip_entry ), "wb" )
                outfile.write ( zip.read( zip_entry ) )
                outfile.close()
        
        # Close zip...
        zip.close()
        
        # Message...
        xbmcgui.Dialog().ok( xbmc.getLocalizedString(31428), xbmc.getLocalizedString(31429) )
        
    except :
        # Message...
        xbmcgui.Dialog().ok( xbmc.getLocalizedString(31428), "Error installing theme.")        
    
#
#
#
main()