package main

import "log"

func main() {
	var isTrue bool
	isTrue = true

	if isTrue {
		log.Println("isTrue is", isTrue)
	} else {
		log.Println("isTrue is", isTrue)
	}

	myVar := "cat"

	switch myVar {
	case "cat":
		log.Println("cat is set to cat")
	case "dog":
		log.Println("cat is set to dog")
	case "fish":
		log.Println("cat is set to fish")
	default:
		log.Println("something else")
	}
}