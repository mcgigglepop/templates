package main

import (
	"log"

	"github.com/mcgigglepop/myniceprogram/helpers"
)

const numPool = 10

func CalculateValue(intChan chan int) {
	randomNumber := helpers.RandomNumber(numPool)
	intChan <- randomNumber
}

func main() {
	intChan := make(chan int)
	defer close(intChan)

	go CalculateValue(intChan)

	num := <-intChan

	log.Println(num)
}

func helpersmain() {
	log.Println("Hello")
	var myVar helpers.SomeType
	myVar.TypeName = "Some Name"
	log.Println(myVar.TypeName)
}
