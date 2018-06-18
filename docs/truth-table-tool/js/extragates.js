/******************************************************************************
 * File: extragates.js
 * Author: Julius Heine (heine.julius@gmail.com)
 *
 * xor and other gates as not and combinations.
 */

/* create text to copy for the formula textbox
 *
 */

function calculate_extra_gates() {
	var inputone = "(" + document.getElementById("extraone").value + ")";
	var inputtwo = "(" + document.getElementById("extratwo").value + ")";
	var gatetype = document.getElementById("gatetype").value;
	var response = "";

	if ((inputone != "") && (inputtwo != "")){
		switch (gatetype) {
			case "xor":
				response = "(!(" + inputone + " and " + inputtwo + ")and(" + inputone + " or " + inputtwo + "))";
				break;
			case "xnor":
				response = "!(!(" + inputone + " and " + inputtwo + ")and(" + inputone + " or " + inputtwo + "))";
				break;
			case "nand":
				response = "!(" + inputone + " and " + inputtwo + ")";
				break;
			
			default:
				console.log("Strange selection");
		  }
	}
	document.getElementById("extraresponse").value = response;
	
}