/******************************************************************************
 * File: customvarsorder.js
 * Author: Julius Heine (heine.julius@gmail.com)
 *
 * Do not order variables alphabetically but in your favourite order.
 */

/* All variables of the formula have to exit in your order expression
 *
 */

function customvarsorder() {
	var varinput = document.getElementById("customvarsorder").value;
	try {		
		return varinput.split(',');
	} catch (e) {		  
		if (e.description !== undefined) {
			displayCompileError(input, e);
		} else {
			throw e;
		}
	}
}