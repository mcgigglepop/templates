package main

import (
	"log"
	"sort"
)

type User struct {
	FirstName string
	LastName string
}

func main() {
	myMap := make(map[string]int)

	myMap["first"] = 1
	myMap["second"] = 2

	myMap2 := make(map[string]User)

	me := User {
		FirstName: "Tom",
		LastName: "Cruise",
	}

	myMap2["me"] = me

	log.Println(myMap["first"], myMap["second"])
	log.Println(myMap2["me"].FirstName)

	slice()
}

func slice(){
	var mySlice []int

	mySlice = append(mySlice, 2)
	mySlice = append(mySlice, 1)
	mySlice = append(mySlice, 3)

	sort.Ints(mySlice)

	numbers := []int{1,2,3,4,5,6}

	log.Println(mySlice)
	log.Println(numbers)
	log.Println(numbers[0:2])

}