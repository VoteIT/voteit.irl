 #!/bin/bash
 #You need lingua and gettext installed to run this
 
 echo "Updating voteit.irl.pot"
 pot-create -d voteit.irl -o voteit/irl/locale/voteit.irl.pot .
 echo "Merging Swedish localisation"
 msgmerge --update voteit/irl/locale/sv/LC_MESSAGES/voteit.irl.po voteit/irl/locale/voteit.irl.pot
 echo "Updated locale files"
 