/******************************************************************************
 * File: truth-table.js
 * Author: Keith Schwarz (htiek@cs.stanford.edu)
 *
 * Logic to generate and display a truth table for parsed representations of
 * propositional logic formulae.
 */
 
/* Function: generateTruthTable
 *
 * Given a parsed representation of a PL formula, computes all possible variable
 * assignments for that formula, determines the value of the formula on each of
 * those assignments, and calls the specified callback to report the results of
 * each of those assignments.
 */
function generateTruthTable(parseResult, callback) {
	/* Create a new array of truth values that will stand for the truth values
	 * of all of the variables. Initially, these values will all be false. We'll
	 * treat this as a binary counter to enumerate all possible truth assignments.
	 */
	var assignment = [];
	for (var i = 0; i < parseResult.variables.length; i++) {
		assignment.push(false);
	}
	
	/* Evaluate the expression under all possible truth values. Remember - even
	 * if there are zero variables, there's still the vacuous truth assignment!
	 */
	do {
		callback(assignment, parseResult.ast.evaluate(assignment));	
	} while (nextAssignment(assignment));
}

/* Function: nextAssignment
 *
 * Given an array representing a truth assignment, generates the next truth
 * assignment from it, returning true if one is found and false otherwise.
 *
 * This implementation works by simulating a binary counter to enumerate all
 * truth values.
 */
function nextAssignment(assignment) {
	/* Walking from the right to the left, search for a false to make true. */
	var flipIndex = assignment.length - 1;
	while (flipIndex >= 0 && assignment[flipIndex]) flipIndex--;
	
	/* If we didn't find an index to flip, we've tried all assignments and are
	 * therefore done.
	 */
	if (flipIndex == -1) return false;
	
	/* Otherwise, flip this index to true and all following values to false. */
	assignment[flipIndex] = true;

	for (var i = flipIndex + 1; i < assignment.length; i++) {
		assignment[i] = false;
	}
	
	return true;
}
