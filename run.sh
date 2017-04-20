#!/bin/bash

# Colours
green='\e[1;32m'
endColor='\e[0m'

for file in ./tests/*
do
    case "$file" in
        *"BFS"* )           echo Running $file | sed -e "s/.txt$//"
                            python3 ThreeDigits.py B $file
                            echo '\n'
                            ;;
        *"DFS"* )           echo Running $file | sed -e "s/.txt$//"
                            python3 ThreeDigits.py D $file
                            ;;
        *"IDS"* )           echo Running $file | sed -e "s/.txt$//"
                            python3 ThreeDigits.py I $file
                            ;;
        *"Greedy"* )        echo Running $file | sed -e "s/.txt$//"
                            python3 ThreeDigits.py G $file
                            ;;
        *"AStar"* )         echo Running $file | sed -e "s/.txt$//"
                            python3 ThreeDigits.py A $file
                            ;;
        *"HillClimbing"* )  echo Running $file | sed -e "s/.txt$//"
                            python3 ThreeDigits.py H $file
                            ;;
    esac
done
