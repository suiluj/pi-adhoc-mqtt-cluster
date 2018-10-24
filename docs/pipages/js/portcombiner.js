/******************************************************************************
 * File: portcombiner.js
 * Author: Julius Heine (heine.julius@gmail.com)
 *
 * xor and other gates as not and combinations.
 */

/* create text to copy for the formula textbox
 *
 */

var urlvernemq = "";
var urlgrafana = "";
var urlchronograf = "";
var urlnodered = "";
var urlprometheus = "";

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

function hostpresetschanged() {
	document.getElementById("host").value = document.getElementById("hostpresets").value;
	go();
	
	
}

function go() {
	var host = document.getElementById("host").value;

	urlvernemq = "http://" + host + ":" + document.getElementById("portvernemq").value;
	urlgrafana = "http://" + host + ":" + document.getElementById("portgrafana").value;
	urlchronograf = "http://" + host + ":" + document.getElementById("portchronograf").value;
	urlnodered = "http://" + host + ":" + document.getElementById("portnodered").value;
	urlprometheus = "http://" + host + ":" + document.getElementById("portprometheus").value;
	
}