//#### Name: Nikita Zolotykh
//#### USCID: 8652729642

#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include "math.h"
using namespace std;

enum Status {UNSOLVED, SOLVED, CONTRADICTION};
string _status[3] = {"Unsolved", "Solved", "Contradiction"};

struct Cell {
	int i, j, k;
	Cell(): i(0), j(0), k(0){}
	Cell(int i1, int j1, int k1): i(i1), j(j1), k(k1){}

	bool operator==(const Cell &other) {
		return (i == other.i && j == other.j && k == other.k);
	}
	bool operator!=(const Cell &other) {
		return !(i == other.i && j == other.j && k == other.k);
	}
};

struct Puzzle {
	vector<vector<Cell> > disjunction;
	vector<Cell> evidence;
	Status status;
	void clearAll()
	{
		disjunction.clear();
		evidence.clear();
		status=UNSOLVED;
	}
};

// This is for Problem 1
Puzzle resolveStrimko(Puzzle &puzzle) {
	int n = sqrt(puzzle.disjunction.size()/4);
	vector<vector<Cell> > setA = puzzle.disjunction;
	vector<Cell> setB = puzzle.evidence;
	vector<Cell> oldSet = setB;

	while (setB.size() < n*n) {
		vector<Cell> newSet;
		for (vector<Cell>::iterator oldSetIterator = oldSet.begin(); oldSetIterator != oldSet.end();) {
			//for all values in the old set
			vector<Cell> negativeSet;
			Cell thisCell = *oldSetIterator;
			vector<vector<Cell> >::iterator disjunctionSetIterator = setA.begin();

			for (int j = 0; j < setA.size(); j++) {
				//generate a set of up to 4(n-1) negative facts for empty cells
				//running through all the disjunctions
				for (vector<Cell>::iterator disjunctionIterator = (*disjunctionSetIterator).begin(); disjunctionIterator != (*disjunctionSetIterator).end();) {
					if (thisCell == (*disjunctionIterator)) {
						//found the same cell in the disjunction
						//remove all the rest and place them into the negative set
						for (vector<Cell>::iterator disjunctionDeleteIterator = (*disjunctionSetIterator).begin(); disjunctionDeleteIterator != (*disjunctionSetIterator).end();) {
							if (*disjunctionDeleteIterator != thisCell) {
								//the cell is different from the one stated in the evidence set
								//delete it and put it into the negative set
								negativeSet.push_back(*disjunctionDeleteIterator);
								(*disjunctionSetIterator).erase(disjunctionDeleteIterator);
							} else {
								++disjunctionDeleteIterator;
							}
						}
						break;
					}
					++disjunctionIterator;
				}
				++disjunctionSetIterator;
			} //at this point, the negative set should be complete

			for (vector<Cell>::iterator negativeSetIterator = negativeSet.begin(); negativeSetIterator != negativeSet.end();) {
				//running through the negative set and all disjunctions, performing removal operations
				for (vector<vector<Cell> >::iterator disjunctionSetIterator = setA.begin(); disjunctionSetIterator != setA.end();) {
					for (vector<Cell>::iterator disjunctionIterator = (*disjunctionSetIterator).begin(); disjunctionIterator != (*disjunctionSetIterator).end();) {
						if (*disjunctionIterator == *negativeSetIterator) {
							(*disjunctionSetIterator).erase(disjunctionIterator);
						} else {
							++disjunctionIterator;
						}
					}
					//look if any d in set A are of size 0
					if ((*disjunctionSetIterator).size() == 0) {
						//|d| = 0
						puzzle.status = CONTRADICTION;
						puzzle.disjunction = setA;
						puzzle.evidence = setB;
						return puzzle;
					}
					++disjunctionSetIterator;
				}
				++negativeSetIterator;
			}
			++oldSetIterator;
		} //end for all the evidence

		for (vector<vector<Cell> >::iterator disjunctionSetIterator = setA.begin(); disjunctionSetIterator != setA.end();) {
			//look if any d in set A are of size 1
			if ((*disjunctionSetIterator).size() == 1) {
				//|d| = 1
				bool foundInB = false;
				bool alreadyInNew = false;
				for (vector<Cell>::iterator it = setB.begin(); it != setB.end();) {
					if ((*disjunctionSetIterator)[0] == *it) {
						//it is already in B
						foundInB = true;
					}
					++it;
				}
				for (vector<Cell>::iterator it = newSet.begin(); it != newSet.end();) {
					if ((*disjunctionSetIterator)[0] == *it) {
						//it is already in B
						alreadyInNew = true;
					}
					++it;
				}
				if (foundInB || alreadyInNew) {
					//it was found in B or new, do not add to the new set
					setA.erase(disjunctionSetIterator);
				} else {
					//it was not found in B, add to the new set
					newSet.push_back((*disjunctionSetIterator)[0]);
					setA.erase(disjunctionSetIterator);
				}
			} else {
				//|d| != 1, keep moving
				++disjunctionSetIterator;
			}
		}

		if (newSet.empty()) {
			puzzle.status = UNSOLVED;
			puzzle.disjunction = setA;
			puzzle.evidence = setB;
			return puzzle;
		}

		for (vector<Cell>::iterator newSetIterator = newSet.begin(); newSetIterator != newSet.end();) {
			//running through the new set and adding it to set B
			//as well as moving everything to the old set
			setB.push_back(*newSetIterator);
			oldSet.clear();
			oldSet = newSet;
			++newSetIterator;
		}
	}
	puzzle.status = SOLVED;
	puzzle.evidence = setB;
	puzzle.disjunction = setA;
	return puzzle;
}

void DFS (Puzzle &original, Puzzle &solution) {
	solution.disjunction = original.disjunction;
	solution = resolveStrimko(solution);
	if (solution.status == SOLVED) {
		return;
	}
	vector<vector<Cell> > setA = solution.disjunction;
	vector<Cell> setB = solution.evidence; //keeps track of current facts
	vector<vector<Cell> > stack; //stack of disjunctions
	stack.push_back(setA.back());

	while (!stack.empty()) {
		//execute while there are disjunctions to explore
		vector<Cell>* v = &stack.back(); //look at a disjunction

		while (!v->empty()) {
			//execute while the current disjunction still has cells to guess
			//making a guess here!
			Cell currentCell = v->back(); //looking at a cell
			v->pop_back();

			//---checking if the cell is already in the set of facts---
			bool alreadyInB = false;
			for (vector<Cell>::iterator it = setB.begin(); it != setB.end();) {
				if (*it == currentCell)
					alreadyInB = true;
				++it;
			}
			//-------------------------------------------------------

			if (alreadyInB == false) {
				//cell is not one of the facts yet
				//add it to the set of facts, and try to solve now!
				setB.push_back(currentCell);
				solution.evidence = setB;
				solution.disjunction = original.disjunction;
				solution = resolveStrimko(solution);

				if (solution.status == SOLVED) //solved, we are done!
					return;
				if (solution.status == CONTRADICTION) {
					//contradiction...
					//remove the last fact that we added, and try with a different cell
					setB.pop_back();
				}
				if (solution.status == UNSOLVED) {
					//unsolved, must go deeper
					break;
				}
			} else {
				//the fact is already in B, keep checking other ones
				solution.status = UNSOLVED;
			}
		}
		//at this point we are done checking the disjunction
		//two ways we can get here:
		//1. we found a cell that wasn't able to solve --- need to look deeper
		//2. no cells in the disjunction worked --- contradiction?...
		//...go back in the search
		
		if (v->empty()) //case 2
			solution.status = CONTRADICTION;
		if (solution.status == CONTRADICTION) {
			//all cells were contradictions!
			//must go back and pick a different cell?
			setB.pop_back();
			stack.pop_back();
			continue;
		}
		if (solution.status == UNSOLVED) {
			//case 1
			//unsolved, must guess again!
			stack.push_back(solution.disjunction.back());
		}
	}
}

// This is for Problem 2
Puzzle solveStrimko(Puzzle &puzzle) {
	Puzzle original = puzzle;
	Puzzle solution = puzzle;
	DFS (original, solution);
	return solution;
}

/// Do not change codes below

void error() {
	cout << "run \'proj1 problem_number\' or \'proj1 problem_number size_id\'" <<endl;
	cout << "\tproblem_number: 1 or 2" <<endl;
	cout << "\tsize_id: 4_1~4_5, 5_1~5_10, 6_1~6_5, 7_1~7_3" <<endl;
}

int main(int argc, char**argv) {
	if (argc < 2){
		error(); return 0;
	}
	vector<string> puzzleNameList;
	if (argc >= 3) {
		puzzleNameList.push_back(argv[2]);
	} else {
		string puzzleNameList_arr[] = {"4_1","4_2","4_3","4_4","4_5","5_1","5_2","5_3","5_4","5_5","5_6","5_7","5_8","5_9","5_10","6_1","6_2","6_3","6_4","6_5","7_1","7_2","7_3"};
		for (int i=0; i<23; ++i)
			puzzleNameList.push_back(puzzleNameList_arr[i]);
	}
	string inputName, outputName, puzzleName; 
	for (int puzzleId=0; puzzleId<puzzleNameList.size(); ++puzzleId){
		puzzleName = puzzleNameList[puzzleId];
#ifdef _WIN32
		inputName = "puzzles\\" + puzzleName + ".txt";
		outputName = "puzzles\\" + puzzleName + ".out";
#else
		inputName = "puzzles/" + puzzleName + ".txt";
		outputName = "puzzles/" + puzzleName + ".out";
#endif
		Puzzle puzzle;
		puzzle.clearAll();
		try {
			ifstream fin;
			fin.open(inputName.c_str());
			if (!fin.is_open())
				throw -1;
			int N, nDis, nEvi;
			fin >> N >> nDis >> nEvi;
			int loc_i, loc_j, num_k;
			for (int i=0; i<nDis; ++i){
				vector<Cell> this_dist;
				this_dist.clear();
				for( int j=0; j<N; ++j) {
					fin >> loc_i >> loc_j >> num_k;
					this_dist.push_back(Cell(loc_i, loc_j, num_k));
				}
				puzzle.disjunction.push_back(this_dist);
			}
			for (int i=0; i<nEvi; ++i)
			{
				fin >> loc_i >> loc_j >> num_k;
				puzzle.evidence.push_back(Cell(loc_i, loc_j, num_k));
			}
			fin.close();
		} catch (...) {
			cout << "Error while loading the puzzle file..." << endl;
			return 1;
		}
		cout << "Puzzle is loaded from " << inputName << endl;	
		Puzzle solution;
		
		switch (argv[1][0]){
			case '1': solution = resolveStrimko(puzzle); break;
			case '2': solution = solveStrimko(puzzle); break;
			case '0': solution = puzzle; break;
			default: error(); return 0;
		}
		try {
			ofstream fout;
			fout.open(outputName.c_str());
			fout << _status[solution.status] << endl;
			fout << solution.evidence.size() << endl;
			for(int i=0; i<solution.evidence.size(); ++i)
			{
				fout << solution.evidence[i].i << " " << solution.evidence[i].j << " " << solution.evidence[i].k << endl;
			}
			fout.close();
		} catch (...){
			cout << "Error while saving the results..." << endl;
			return 1;
		}
		cout << "Solution is saved in " << outputName << endl;	
	}
	return 0;
}
