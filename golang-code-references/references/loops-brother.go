package main

import "log"

func main() {
	for i := 0; i <= 10; i++ {
		log.Println(i)
	}

	slices()
	slicesNon()
	mapNon()
	mapp()
	strings()
	structs()
}

func slices() {
	animals := []string{"dog", "cat", "horse", "cow", "cat"}

	for i, animal := range animals {
		log.Println(i, animal)
	}
}

func slicesNon() {
	animals := []string{"dog", "cat", "horse", "cow", "cat"}

	for _, animal := range animals {
		log.Println(animal)
	}
}

func mapNon() {
	animals := make(map[string]string)

	animals["dog"] = "Fido"
	animals["cat"] = "Fluffy"

	for _, animal := range animals {
		log.Println(animal)
	}
}

func mapp() {
	animals := make(map[string]string)

	animals["dog"] = "Fido"
	animals["cat"] = "Fluffy"

	for animalType, animal := range animals {
		log.Println(animalType, animal)
	}
}

func strings() {
	var myString = "this is a string"

	for i, l := range myString {
		log.Println(i, " ", l)
	}
}

func structs() {
	type User struct {
		FirstName string
		LastName  string
		Email     string
		Age       int
	}

	var users []User
	users = append(users, User{"Tom", "Cruise", "tc@email.com", 60})
	users = append(users, User{"Tom", "Bruise", "tb@email.com", 61})
	users = append(users, User{"Tom", "Snooze", "ts@email.com", 62})
	users = append(users, User{"Tom", "Lose", "tl@email.com", 63})

	for _, l := range users {
		log.Println(l.FirstName, l.LastName, l.Email, l.Age)
	}
}
