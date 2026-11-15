package lexer

import (
	"bytes"
	"go-compiler/lexer"
)

type Lexer struct {
	input        string
	position     int  // current position of input
	readPosition int  // next reading position
	ch           byte // current character under examination
}

func (l *Lexer) readChar() {
	if l.readPosition >= len(l.input) {
		l.ch = 0 // EOF
	} else {
		l.ch = l.input[l.readPosition]
	}
	l.position = l.readPosition
	l.readPosition += 1
}

func New(input string) *Lexer {
	l := &Lexer{input: input}
	l.readChar()
	return l
}

func isDigit(digit byte) bool {
	if digit >= '0' && digit <= '9' {
		return true
	}
	return false
}

func lowerCaseByte(char byte) byte {
	charSlice := []byte{char}
	charSlice = bytes.ToLower((charSlice))
	return charSlice[0]
}

func isLetter(char byte) bool {
	char = lowerCaseByte(char)
	if char >= 'a' && char <= 'z' {
		return true
	}
	return false
}

func NextToken(l *Lexer) Token {
	switch l.ch {
	case '=':
		return Token{lexer.ASSIGN, "="}
	case '+':
		return Token{lexer.PLUS, "+"}
	case '-':
		return Token{lexer.MINUS, "-"}
	case '*':
		return Token{lexer.MULTIPLY, "*"}
	case '/':
		return Token{lexer.DIVIDE, "/"}
	case '(':
		return Token{lexer.LPAREN, "("}
	case ')':
		return Token{lexer.RPAREN, ")"}
	case '\n':
		return Token{lexer.NEWLINE, "\n"}
	default:
	}
	if isLetter(l.ch) {

	} else if isDigit(l.ch) {

	}
	return Token{lexer.UNKNOWN, ""}
}
