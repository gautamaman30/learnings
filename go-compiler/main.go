package main

import (
	"go-compiler/lexer"
)

func main() {
	input := "x = 5\ny = x + 3\nprint y"
	lexer := lexer.New(input)
}
