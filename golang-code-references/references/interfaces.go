package main

import "fmt"

// similar to a class that returns methods
type Animal interface {
	Says() string
	NumberOfLegs() int
}

type Dog struct {
	Name  string
	Breed string
}

type Gorilla struct {
	Name          string
	Color         string
	NumberOfTeeth int
}

func main() {
	dog := Dog{
		Name:  "Samson",
		Breed: "German Shepherd",
	}

	// passing in a struct reference
	PrintInfo(&dog)

	gorilla := Gorilla{
		Name:  "Jock",
		Color: "grey",
		NumberOfTeeth: 38,
	}

	PrintInfo(&gorilla)
}

// receives the custom interface
func PrintInfo(a Animal) {
	// call the custom interface methods from the custom interface
	fmt.Println("This anmial says", a.Says(), "and has", a.NumberOfLegs(), "legs")
}

// custom interface methods for each animal
func (d *Dog) Says() string {
	return "woof"
}

func (d *Dog) NumberOfLegs() int {
	return 4
}

func (d *Gorilla) Says() string {
	return "ugh"
}

func (d *Gorilla) NumberOfLegs() int {
	return 2
}