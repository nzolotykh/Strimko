# Strimko (AI Project)

*NOTES*

This is a project for the CSCI 360 Introduction to Artificial Intelligence class with Professor Sven Koenig. My code can be found in proj2.cpp. The project is for educational purposes only.

Strimko is a puzzle similar to Sudoku, but instead of having the requirement to place numbers 1-9 in nine 3x3 squares, Strimko has a different requirement of placing the numbers in certain "streams". This program utilizes the concepts of constraints satisfaction and knowledge representation to resolve and completely solve Strimko puzzles. Other search algorithms such as DFS and Backtracking were also used in this algorithm. By extension, the program can also solve Sudoku puzzles (though examples of Sudoku puzzles are not provided). Separate Python-based application is used to visualize the results of my algorithm.

*INSTRUCTIONS*

Compile proj2.cpp using g++ or equivalent. When running the program, make sure to provide "2" as the argument to solve all of the provided problems. The argument just tells the program which function from proj2.cpp to execute, and only solveStrimko() completely solves all of the puzzles. Once solved, you can visualize the results using the provided Python program by executing python GUI.py in the command line.