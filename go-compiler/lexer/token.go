package lexer

type TokenType int

const (
	IDENTIFIER TokenType = iota
	NUMBER
	ASSIGN
	PLUS
	MINUS
	MULTIPLY
	DIVIDE
	LPAREN
	RPAREN
	PRINT
	NEWLINE
	EOF
)

type Token struct {
	Type    TokenType
	Literal string
}

func (t TokenType) String() string {
	switch t {
	case IDENTIFIER:
		return "IDENTIFIER"
	case NUMBER:
		return "NUMBER"
	case ASSIGN:
		return "ASSIGN"
	case PLUS:
		return "PLUS"
	case MINUS:
		return "MINUS"
	case MULTIPLY:
		return "MULTIPLY"
	case DIVIDE:
		return "DIVIDE"
	case LPAREN:
		return "LPAREN"
	case RPAREN:
		return "RPAREN"
	case PRINT:
		return "PRINT"
	case NEWLINE:
		return "NEWLINE"
	case EOF:
		return "EOF"
	default:
		return "UNKNOWN"
	}
}
