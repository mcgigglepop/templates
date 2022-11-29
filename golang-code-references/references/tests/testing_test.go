package main

import "testing"

// table tests
var tests = []struct {
	name     string
	dividend float32
	divisor  float32
	expected float32
	isErr    bool
}{
	{"valid-data", 100.0, 10.0, 10.0, false},
	{"invalid-data", 100.0, 0.0, 0.0, true},
	{"expect-5", 50.0, 10.0, 5.0, false},
}

func TestDivision(t *testing.T) {
	for _, tt := range tests {
		got, err := divide(tt.dividend, tt.divisor)
		if tt.isErr {
			// there is an error
			if err == nil {
				t.Error("Expected an error but did not get one")
			}
		} else {
			// there is not an error
			if err != nil {
				t.Error("did not expect an error but got one:", err.Error())
			}
		}
		// if the result "got" is not equal to our expected value (assigned above)
		if got != tt.expected {
			t.Errorf("Expected %f but got %f", tt.expected, got)
		}
	}
}

//manual tests
func TestDivide(t *testing.T) {
	_, err := divide(10.0, 1.0)
	if err != nil {
		t.Error("got an error when we should not have")
	}
}

func TestBadDivide(t *testing.T) {
	_, err := divide(10.0, 0.0)
	if err == nil {
		t.Error("did not get an error when we should have")
	}
}

// go test
// go test -v
// go test cover
// go test -coverprofile=coverage.out && go tool cover -html=coverage.out
