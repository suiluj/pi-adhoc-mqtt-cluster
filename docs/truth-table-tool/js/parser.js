/******************************************************************************
 * File: parser.js
 * Author: Keith Schwarz (htiek@cs.stanford.edu)
 *
 * A parser that produces an AST from a sequence of tokens.
 */
 
/* Function: parse
 *
 * Given an input string, parses it to produce an AST and variable map. If
 * successful, the returned object will have these fields:
 *
 *   ast:       The root of the generated AST.
 *   variables: A map from indices to variables.
 *
 * On failure, this function throws an exception with these fields:
 *
 *   description: What went wrong?
 *   start:       Start index of the syntax error.
 *   end:         End index of the syntax error.
 */
function parse(input) {
	/* Scan the input to get the tokens and the variable map. */
	var scanResult = scan(input);
	var tokens = scanResult.tokens;
	
	/* Use Dijkstra's shunting-yard algorithm to convert from infix to postfix,
	 * building the AST as we go. This means we need to track the operators and
	 * operands (where the operands stack also includes parentheses.)
	 *
	 * The ~ operator is odd in that it modifies something we haven't seen yet.
	 * To handle this, we push it onto the operands stack. Whenever we read
	 * an operand, we repeatedly pop off negations until none remain.
	 */
	var operators   = [];
	var operands    = [];
	
	/* We can be in one of two different states:
	 *
	 *  needOperand: We're expecting something that ultimately evaluates to an expression. This can be
	 *               T, F, a variable, a negation of something, or a parenthesis.
	 * !needOperand: We've got the operand, and now we're expecting an operator to be applied to it. We
	 *               can also get a close parenthesis.
	 *
	 */
	var needOperand = true;
	
	/* Scan across the tokens! */
	for (var i in tokens) {
		var currToken = tokens[i];
		
		if (needOperand) {
			/* If it's an operand, push it on the operand stack. */
			if (isOperand(currToken)) {
				addOperand(wrapOperand(currToken), operands, operators);
				needOperand = false;
			}
			/* If it's a parenthesis or negation, push it on the parenthesis stack. We're
			 * still expecting an operand.
			 */
			else if (currToken.type === "(" || currToken.type === "~") {
				operators.push(currToken);
			}
			
			/* It's also possible that we have hit the end of the input. This is an error,
			 * but to be nice, we'll give a more specific error condition.
			 */
			else if (currToken.type === kScannerConstants.EOF) {
				/* If the operator stack is empty, the input was empty. */
				if (operators.length === 0) {
					parseError("", 0, 0);
				}
								
				/* If the operator stack has an ( on top, there's an unmatched open parenthesis. */
				if (topOf(operators).type === "(") {
					parseError("This open parenthesis has no matching close parenthesis.",
					           topOf(operators).start, topOf(operators).end);
				}
				
				/* Otherwise, it's an operator with no operand. */
				parseError("This operator is missing an operand.",
				           topOf(operators).start, topOf(operators).end);
			}
			/* Anything else is a parse error. */
			else {
				parseError("We were expecting a variable, constant, or open parenthesis here.",
				           currToken.start, currToken.end);
			}
		}
		/* Otherwise, we're expecting either an operator or a close parenthesis. */
		else {		
			/* If this is an operator, eagerly evaluate operators until this one
			 * has priority no lower than what comes before it. As a trick/hack, we
			 * treat EOF as an operator with lowest priority, so upon hitting EOF
			 * we forcibly evaluate everything.
			 */
			if (isBinaryOperator(currToken) || currToken.type === kScannerConstants.EOF) {
				/* While there are higher-priority operators atop the stack,
				 * evaluate them.
				 */
				while (true) {
					/* If there are no more operands to evaluate, we're done. */
					if (operators.length === 0) break;
					
					/* If it's an open parenthesis, we should stop because the current
					 * operator is being parenthesized for later us.
					 */
					if (topOf(operators).type === "(") break;
					
					/* Compare the priority of the stack top to the priority of the current
					 * operator. We stop if the new operator has priority greater than or
					 * equal to the current operator to ensure rightmost grouping.
					 */
					if (priorityOf(topOf(operators)) <= priorityOf(currToken)) break;
				
					/* Otherwise, evaluate the operator atop the stack. */
					var operator = operators.pop();
					var rhs = operands.pop();
					var lhs = operands.pop();
					
					addOperand(createOperatorNode(lhs, operator, rhs), operands, operators);
				}
				
				/* Now, push this operator onto the operators stack. */
				operators.push(currToken);
				
				/* We just read our operator, so now we're expecting an operand. */
				needOperand = true;
				
				/* At this point, if we got EOF, stop. */
				if (currToken.type === kScannerConstants.EOF) break;
			}
			
			/* If this is a close parenthesis, we pop operators from the stack and
			 * evaluate them until we come to an open parenthesis. We then still are
			 * searching for an operator.
			 */
			else if (currToken.type === ")") {
				/* Keep popping operators until we get a close parenthesis. */
				while (true) {
					/* If we ran out of operators, we have a mismatched parenthesis. */
					if (operators.length === 0) {
						parseError("This close parenthesis doesn't match any open parenthesis.", currToken.start, currToken.end);
					}
					var currOp = operators.pop();
				
					/* If the top of the stack is an open parenthesis, we should have the
					 * top of the operand stack containing our value, so we're done.
					 */
					if (currOp.type === "(") break;
					
					/* Otherwise, if the top of the stack is a negation, we have a syntax error. */
					if (currOp.type === "~") {
						parseError("Nothing is negated by this operator.", currOp.start, currOp.end);
					}
					
					/* Otherwise, it should be an operator. Evaluate it. */
					var rhs = operands.pop();
					var lhs = operands.pop();
					
					addOperand(createOperatorNode(lhs, currOp, rhs), operands, operators);
				}
				
				/* At this point, the stack top contains the operand produced from the parenthesized
				 * expression, but we didn't expose it to any negations. Therefore, we'll pop it and
				 * add it back through addOperand.
				 */
				var expr = operands.pop();
				addOperand(expr, operands, operators);
			}
			/* Anything else is an error. */
			else {
				parseError("We were expecting a close parenthesis or a binary connective here.",
				           currToken.start, currToken.end);
			}
		}
	}
	
	/* We've now successfully parsed the input, but there may be extra junk on
	 * the stack to worry about. We'll handle that here.
	 */
	
	/* These are effectively asserts that the top of the stack is EOF; they
	 * should never fail unless there's an error case we forgot to handle
	 * above.
	 */
	assert (operators.length !== 0, "No operators on the operator stack (logic error in parser?)");
	assert (operators.pop().type === kScannerConstants.EOF, "Stack top is not EOF (logic error in parser?)");
	
	/* The operators stack should now be empty. */
	if (operators.length !== 0) {
		/* The top should be an open parenthesis, since EOF would have evicted
		 * anything else.
		 */
		var mismatchedOp = operators.pop();
		assert (mismatchedOp.type === "(", 
		        "Somehow missed an operator factoring in EOF (logic error in parser?)");
		        
		parseError("No matching close parenthesis for this open parenthesis.",
		           mismatchedOp.start, mismatchedOp.end);
	}
	
	/* If we're here, we did the parse successfully! The top of the operands stack is our
	 * AST root, and the information from the scan gives us the variables map.
	 */
	return {
	   ast:       operands.pop(),
	   variables: scanResult.variables
	};
}

/* Function: addOperand
 *
 * Adds a new operand to the operands stack, evaluating any negations that need to be
 * performed first.
 */
function addOperand(node, operands, operators) {
	/* Keep evaluating negate operators until none remain. */
	while (operators.length > 0 && topOf(operators).type === "~") {
		operators.pop();
		node = new negateNode(node);
	}
	
	/* At this point, we've negated as much as possible. Add the new AST node
	 * to the operands stack.
	 */
	operands.push(node);
}

/* Function: isOperand
 *
 * Returns whether the given token is an operand. The operands are T, F, and variables.
 */
function isOperand(token) {
	return token.type === "T" ||
	       token.type === "F" ||
	       token.type === "variable";
}

/* Function: wrapOperand
 *
 * Given an operand token, returns an AST node encapsulating that operand.
 */
function wrapOperand(token) {
	if (token.type === "T")	return new trueNode();
	if (token.type === "F") return new falseNode();
	if (token.type === "variable") return new variableNode(token.index);
	unreachable("Token " + token.type + " isn't an operand.");
}

/* Function: isBinaryOperator
 *
 * Given a token, reports whether the token is a binary operator.
 */
function isBinaryOperator(token) {
	return token.type === "<->" ||
	       token.type === "->"  ||
	       token.type === "/\\" ||
	       token.type === "\\/";
}

/* Function: priorityOf
 *
 * Returns the priority of the given operator. We pretend that EOF is an operator
 * with minimal priority to ensure that when EOF is seen, we pop off all remaining
 * operators.
 */
function priorityOf(token) {
	if (token.type === kScannerConstants.EOF) return -1;
	if (token.type === "<->") return 0;
	if (token.type === "->")  return 1;
	if (token.type === "\\/") return 2;
	if (token.type === "/\\") return 3;
	unreachable("Should never need the priority of " + token.type);
}

/* Function: createOperatorNode
 *
 * Given the LHS and RHS of an expression and the token reprsenting the operator,
 * creates an AST node corresponding to that operator.
 */
function createOperatorNode(lhs, token, rhs) {
	if (token.type === "<->") return new iffNode(lhs, rhs);
	if (token.type === "->")  return new impliesNode(lhs, rhs);
	if (token.type === "\\/") return new orNode(lhs, rhs);
	if (token.type === "/\\") return new andNode(lhs, rhs);
	unreachable("Should never need to create an operator node from " + token.type);
}

/* Function: topOf
 *
 * Returns the last element of an array.
 */
function topOf(array) {
	assert(array.length !== 0, "Can't get the top of an empty array.");
	return array[array.length - 1];
}

/* Function: parseError
 *
 * Triggers a failure of the parser on the specified range of characters.
 */
function parseError(why, start, end) {
	throw { "description": why,
	        "start":  start,
	        "end":    end };
}
