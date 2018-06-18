/******************************************************************************
 * File: renderer.js
 * Author: Keith Schwarz (htiek@cs.stanford.edu)
 *
 * Logic to display results and information to the user.
 */

/* Function: prettyPrintTruthTable
 *
 * Outputs an elegantly-formatted truth table for the given parsed expression.
 */
function prettyPrintTruthTable(parseResult) {
	var table = createTableElement();
	
	/* Create the header, which needs knowledge of the variables and the expression. */
	createTableHeader(table, parseResult);
	
	/* Now, go generate the body of the table. */
	generateTruthTable(parseResult, outputRow(table));
	
	/* Display the table. */
	displayTable(table);
}

/* Function: createTableElement
 *
 * Creates a new table element and sets up its properties.
 */
function createTableElement() {
	var result = document.createElement("table");
	result.className = "truthTable";
	return result;
}

/* Function: createTableHeader
 *
 * Given a table representing the result of the truth table, creates the header
 * for the table by listing the variables and the expression in separate columns.
 */
function createTableHeader(table, parseResult) {
	var header = document.createElement("tr");
	header.className = "header";

	/* Add one column for each variable. */
	for (var i = 0; i < parseResult.variables.length; i++) {
		var cell = document.createElement("th");
		cell.className = "variable";
		cell.innerHTML = parseResult.variables[i];
		header.appendChild(cell);
	}
	
	/* Add one column for the overall expression. */
	var lastCell = document.createElement("th");
	lastCell.className = "expression";
	lastCell.innerHTML = parseResult.ast.toString(parseResult.variables);
	header.appendChild(lastCell);

	table.appendChild(header);
} 
 
/* Function: outputRow
 *
 * Given a table to output a row to, creates a callback that outputs a row to that table.
 */
function outputRow(table) {
	return function(assignment, result) {
		var row = document.createElement("tr");
		
		/* Show the value of each variable. */
		for (var i = 0; i < assignment.length; i++) {
			var cell = document.createElement("td");
			//cell.innerHTML = (assignment[i]? "T" : "F");
			cell.innerHTML = (assignment[i]? "1" : "0");
			row.appendChild(cell);
		}
		
		/* Show the value of the expression. */
		var lastCell = document.createElement("td");
		//lastCell.innerHTML = (result? "T" : "F");
		lastCell.innerHTML = (result? "1" : "0");
		row.appendChild(lastCell);
		
		table.appendChild(row);
	}
}

/* Function: displayTable
 *
 * Displays the specified truth table in the window.
 */
function displayTable(table) {
	/* Create a container div to hold the table. */
	var holder = document.createElement("div");
	holder.className = "truth-table-holder";
	holder.appendChild(table);
	
	showObject(holder);
}

/* Function: showObject
 *
 * Displays the specified HTML object in the output box.
 */
function showObject(object) {
	/* Find the div to hold the object. */
	var target = document.getElementById("table-target");
	
	/* If it already has objects, remove them. */
	while (target.children.length !== 0) {
		target.removeChild(target.children[0]);
	}
	
	/* Install our object in that spot. */
	target.appendChild(object);
}

/* Function: displayCompileError
 *
 * Displays the specified compilation error message. The first parameter should
 * be the actual string provided as input, and the second the error message
 * that was generated.
 */
function displayCompileError(input, error) {
	/* Create a div to hold the result. */
	var holder = document.createElement("div");
	
	/* Create the top div, which shows the original input. */
	holder.appendChild(createHighlightedErrorBox(input, error));
	holder.appendChild(createDescriptionBox(error));
	
	showObject(holder);
}

/* Function: createHighlightedErrorBox
 *
 * Given the text input and the reported error information, creates an HTML
 * element highlighting the given error.
 */
function createHighlightedErrorBox(input, error) {
	/* Create a div to house the result. */
	var box = document.createElement("div");
	box.className = "syntax-error-holder";
	
	/* Create a span of the characters up to, but not including, the actual error. */
	var prefix = document.createElement("span");
	prefix.className = "syntax-okay";
	prefix.textContent = input.substring(0, error.start);
	
	/* Create a span of the characters containing the error. */
	var problem = document.createElement("span");
	problem.className = "syntax-error";
	problem.textContent = input.substring(error.start, error.end);
	
	/* Create a span of characters containing everything after the error. */
	var suffix = document.createElement("span");
	suffix.className = "syntax-okay";
	suffix.textContent = input.substring(error.end);
	
	box.appendChild(prefix);
	box.appendChild(problem);
	box.appendChild(suffix);
	return box;
}

/* Function: createDescriptionBox
 *
 * Given an error, creates an HTML box containing that error.
 */
function createDescriptionBox(error) {
	var box = document.createElement("div");
	box.className = "syntax-error-explanation";
	box.textContent = error.description;
	return box;
}
