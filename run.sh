#!/bin/bash

# Colours
Black='\e[0;30m';
Red='\e[0;31m';
Green='\e[0;32m';
Yellow='\e[0;33m';
Blue='\e[0;34m';
Purple='\e[0;35m';
Cyan='\e[0;36m';
White='\e[0;37m';

# Colour reset
ResetColour='\e[0m';

echo Zipping ${Cyan}ThreeDigits.py Queue.py State.py ${ResetColour}. . .${Blue}
rm ~/Desktop/comp3308assignment1jver0769.zip
zip comp3308assignment1jver0769.zip ThreeDigits.py Queue.py State.py
mv comp3308assignment1jver0769.zip ~/Desktop/
echo "\n";

for file in ./tests/*.txt
do
    # print output to tell which test is being executed
    prefix='.\/tests\/test';
    suffix='.txt';
    prompt=`echo $file | sed -e "s/^$prefix//" -e "s/$suffix$//"`;
    echo -e "${Green}Running ${Purple}${prompt} ${ResetColour}"

    # execute test
    case "$file" in
        *"BFS"* )           python3 ThreeDigits.py B $file
                            ;;
        *"DFS"* )           python3 ThreeDigits.py D $file
                            ;;
        *"IDS"* )           python3 ThreeDigits.py I $file
                            ;;
        *"Greedy"* )        python3 ThreeDigits.py G $file
                            ;;
        *"AStar"* )         python3 ThreeDigits.py A $file
                            ;;
        *"HillClimbing"* )  python3 ThreeDigits.py H $file
                            ;;
        * )
                            break
                            ;;
    esac
    echo '\n';
done

exit 0
