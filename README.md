# thunar-custom-actions-miro
My thunar custom actions
- -----------------------------------------------
- Each custom action has a script file (.py/.sh) and an "-info.txt" file 
  - Some custom actions that do no require a script will only have an "-info.txt" file
- -----------------------------------------------
- Put the script you want to add in /usr/local/bin/Thunar (if there is one)
- The "-info.txt" file contains the command needed for the custom action to work and other attributes
  - It also contains the required dependencies, if any
- -----------------------------------------------
- Feel free to assign custom keyboard shortcuts and icons to your custom actions
- Thunar saves your custom actions config in ~/.config/Thunar in files "uca.xml" (custom actions), and "accels.scm" (keyboard shortcuts)
