// 1. transform the struct to protocol buffer
// 2. send protobuf message via HTTP to so some server
// 3. In the server side, read that message and transform back into that initial

package main

import (
	"fmt"

	"github.com/DeDiS/protobuf"
)

type Person struct {
	Name  string
	Id    int32
	Email *string
	Phone map[string]PhoneNumber
}

type PhoneType uint32

const (
	MOBILE PhoneType = iota
	HOME
	WORK
)

type PhoneNumber struct {
	Number      string
	CountryCode string
}

func main() {
	email := "john.doe@example.com"
	// mobile := MOBILE
	// work := WORK
	phoneNumbers := make(map[string]PhoneNumber)
	phoneNumbers["mobile"] = PhoneNumber{
		Number:      "00000",
		CountryCode: "+1",
	}
	phoneNumbers["work"] = PhoneNumber{
		Number:      "11111",
		CountryCode: "+2",
	}

	person := Person{
		Name:  "John Doe",
		Id:    123,
		Email: &email,
		Phone: phoneNumbers,
	}

	//fmt.Println(person)

	buf, err := protobuf.Encode(&person)
	if err != nil {
		fmt.Println("hit first error")
		fmt.Println(err.Error())
	} else {
		//fmt.Println(string(buf))

		var person2 Person
		err = protobuf.Decode(buf, &person2)
		if err != nil {
			fmt.Println(err.Error())
		} else {
			fmt.Printf("%+v\n", person2)
		}

	}

}
