#
# ThemeInstaller script by Dan Dar3
# Instals and applies skin themes from local or remote zip files
#
# Imports
#
import os
import re
import glob
import fnmatch
import zipfile
import urllib
import xbmc
import xbmcgui

#
# Init
#
if os.getenv("OS") == "xbox" :
    SKIN_PATH = os.path.join( xbmc.translatePath("special://home/skin"), xbmc.getSkinDir() )
else:
    SKIN_PATH = os.path.join( xbmc.translatePath("special://home/addons"), xbmc.getSkinDir() )

SKIN_THEMES_PATH = os.path.join( SKIN_PATH, "extras", "themes" ) 
SKIN_MEDIA_PATH  = os.path.join( SKIN_PATH, "media" )
SKIN_COLORS_PATH = os.path.join( SKIN_PATH, "colors" )

#
# Main
#
def main() :
    SKIN_THEMES_REPO = None
    if len(sys.argv) == 2 and sys.argv[ 1 ].startswith("http://") :
        SKIN_THEMES_REPO = sys.argv[ 1 ]

    #
    # Get a list of local themes...
    #
    themes = get_local_themes()

    # Add entry to download more themes...
    themes.append( xbmc.getLocalizedString(31812) )

    #
    # Dialog to select local theme or download more...
    #
    dialogThemes = xbmcgui.Dialog()
    index        = dialogThemes.select( xbmc.getLocalizedString(31428), themes ) 

    #
    # Cancel / Back...
    #
    if index == -1 :
        return
    #
    # Download more themes...
    #
    elif index == len( themes ) - 1 :
        show_remote_themes( SKIN_THEMES_REPO )
    #
    # Install local theme...
    #
    else :
        theme   = themes[ index ]
        install_local_theme( theme )

#
# Get local themes
#
def get_local_themes( ) :
    #
    # Get a list of extra themes (local)
    #       
    themes = []
    
    if os.path.isdir( SKIN_THEMES_PATH ) :
        for entry in os.listdir( SKIN_THEMES_PATH ) :
            if fnmatch.fnmatch(entry, "*.zip") :
                ( name, ext ) = os.path.splitext( entry )
                themes.append( name )
    
    # Return value
    return themes

#
# Show remote themes
#
def show_remote_themes( skin_themes_repo ) :
    file = urllib.urlopen( skin_themes_repo )
    html = file.read()
    
    # Parse HTML...
    regexp = re.compile( "<li><a href=\"(.*?)\">(.*?)</a></li>", re.DOTALL )
    items  = regexp.findall( html )
    
    # Build a list of remote themes...
    themes = []
    for item in items :
       if item[1] != ".." :
           ( name, ext ) = os.path.splitext( item[1] )
           themes.append( name )

    # No remote themes found...
    if len( themes ) == 0 :
        xbmcgui.Dialog().ok( xbmc.getLocalizedString(31428), xbmc.getLocalizedString(31431) )
    # User to choose a remote theme...
    else :
        dialogThemes = xbmcgui.Dialog()
        index = dialogThemes.select( xbmc.getLocalizedString(31428), themes )

        # Cancel...
        if index == -1 :
            return
        
        #  User chose remote theme...
        theme = themes[ index ]
        
        # Show progress dialog...
        dp = xbmcgui.DialogProgress()
        dp.create( xbmc.getLocalizedString(31428), xbmc.getLocalizedString(31432), theme )
        
        # Download theme...
        remote_theme = os.path.join( skin_themes_repo, "%s.zip" % theme )
        local_theme  = os.path.join( SKIN_THEMES_PATH, "%s.zip" % theme )
        urllib.urlretrieve( remote_theme, local_theme, lambda nb, bs, fs, url=remote_theme : download_progress_hook( nb, bs, fs, local_theme, dp ) )
        
        # Close progress dialog...
        dp.close()
        
        # Install local theme...
        install_local_theme( theme )

#
# Download progress hook...
#
def download_progress_hook( numblocks, blocksize, filesize, url=None, dp=None, ratio=1.0 ):
    downloadedsize  = numblocks * blocksize
    percent         = int( downloadedsize * 100 / filesize )
    
    dp.update( percent )

#
# Install local theme
#
def install_local_theme( theme ) :
    try :
        # Init
        themeZip = os.path.join( SKIN_THEMES_PATH, "%s.zip" % theme )
    
        # Extract theme zip...
        zip = zipfile.ZipFile (themeZip, "r")
        for zip_entry in zip.namelist() :
        
            # XML - skin/color
            if zip_entry == "%s.xml" % theme :
                outfile = open( os.path.join( SKIN_COLORS_PATH, zip_entry ), "wb" )
                outfile.write ( zip.read( zip_entry ) )
                outfile.close()
                
            # XPR - skin/media
            elif zip_entry == "%s.xpr" % theme :
                outfile = open( os.path.join( SKIN_MEDIA_PATH, zip_entry ), "wb" )
                outfile.write ( zip.read( zip_entry ) )
                outfile.close()
                
            # XBT - skin/media
            elif zip_entry == "%s.xbt" % theme :
                outfile = open( os.path.join( SKIN_MEDIA_PATH, zip_entry ), "wb" )
                outfile.write ( zip.read( zip_entry ) )
                outfile.close()
        
        # Close zip...
        zip.close()
        
        # Message...
        #xbmcgui.Dialog().ok( xbmc.getLocalizedString(31428), xbmc.getLocalizedString(31429) )
        
        # Apply theme...
        choice = xbmcgui.Dialog().yesno(xbmc.getLocalizedString(31428), xbmc.getLocalizedString(31441))
        if choice == True :
            xbmc.executehttpapi( "SetGUISetting(3;lookandfeel.skintheme;%s)"  % theme )
            xbmc.executehttpapi( "SetGUISetting(3;lookandfeel.skincolors;%s)" % theme )
            xbmc.executebuiltin( "XBMC.ReloadSkin()")
        
    except :
        # Message...
        xbmcgui.Dialog().ok( xbmc.getLocalizedString(31428), "Error installing theme.")        
    
#
#
#
main()