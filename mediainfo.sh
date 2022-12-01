#!/bin/bash

mediainfo --Output=$'General;%FileNameExtension%\\r\\n%Duration/String3%\\r\\n%FileSize/String%\nVideo;\\r\\n%Width%x%Height%\\r\\n%DisplayAspectRatio/String%\\r\\n%FrameRate/String%\\r\\n%BitRate/String%\nAudio;\\r\\n\\r\\nAduio %StreamKindPos%\\r\\n%BitRate/String%\\r\\n%Channel(s)/String%\\r\\n%ChannelLayout%\\r\\n%Language/String%' "$1";
echo "";
read -p "TYPE 'f' FOR FULL INFO" userInput;
if [[ "$userInput" != "f" ]]; then exit 0; fi
clear;
mediainfo "$1";
read holdTerminal;
