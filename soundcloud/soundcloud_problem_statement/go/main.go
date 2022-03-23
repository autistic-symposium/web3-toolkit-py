package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"net"
	"strconv"
	"strings"
)

const eventPort = 9090
const clientPort = 9099

func main() {
	clientPool := make(map[int]net.Conn)
	followRegistry := map[int]map[int]bool{}

	seqNoToMessage := make(map[int][]string)

	go func() {
		lastSeqNo := 0

		eventListener, err := net.Listen("tcp", fmt.Sprintf("127.0.0.1:%d", eventPort))
		if err != nil {
			log.Fatal(err)
		}
		defer eventListener.Close()

		fmt.Printf("Listening for events on %d\n", eventPort)

	outer:
		for {
			conn, err := eventListener.Accept()

			if err != nil {
				log.Fatal(err)
			}
			defer conn.Close()

			reader := bufio.NewReader(conn)

			for {
				payloadRaw, err := reader.ReadString('\n')

				if err == io.EOF {
					conn.Close()
					continue outer

				} else if err != nil {
					log.Fatal(err)
				}

				payload := strings.TrimSpace(payloadRaw)

				fmt.Printf("Message received: %s\n", payload)

				payloadParts := strings.Split(payload, "|")

				incomingSeqNo, err := strconv.Atoi(payloadParts[0])
				if err != nil {
					log.Fatal(err)
				}

				seqNoToMessage[incomingSeqNo] = payloadParts

				for {

					nextMessage, ok := seqNoToMessage[lastSeqNo+1]
					delete(seqNoToMessage, lastSeqNo+1)

					if !ok {
						break
					}

					nextPayload := strings.Join(nextMessage, "|") + "\n"
					kind := strings.TrimSpace(nextMessage[1])

					switch kind {
					case "F":
						fromUserID, err := strconv.Atoi(nextMessage[2])
						if err != nil {
							log.Fatal(err)
						}
						toUserID, err := strconv.Atoi(nextMessage[3])
						if err != nil {
							log.Fatal(err)
						}

						if _, ok := followRegistry[toUserID]; !ok {
							followRegistry[toUserID] = make(map[int]bool)
						}

						followers, _ := followRegistry[toUserID]
						followers[fromUserID] = true

						clientConn, ok := clientPool[toUserID]
						if ok {
							fmt.Fprint(clientConn, nextPayload)
						}

					case "U":
						fromUserID, err := strconv.Atoi(nextMessage[2])
						if err != nil {
							log.Fatal(err)
						}
						toUserID, err := strconv.Atoi(nextMessage[3])
						if err != nil {
							log.Fatal(err)
						}

						if followers, ok := followRegistry[toUserID]; ok {
							delete(followers, fromUserID)
						}

					case "P":
						toUserID, err := strconv.Atoi(nextMessage[3])
						if err != nil {
							log.Fatal(err)
						}

						if clientConn, ok := clientPool[toUserID]; ok {
							fmt.Fprint(clientConn, nextPayload)
						}

					case "B":
						for _, clientConn := range clientPool {
							fmt.Fprint(clientConn, nextPayload)
						}

					case "S":
						fromUserID, err := strconv.Atoi(nextMessage[2])
						if err != nil {
							log.Fatal(err)
						}

						if followers, ok := followRegistry[fromUserID]; ok {
							for follower := range followers {
								clientConn, ok := clientPool[follower]
								if ok {
									fmt.Fprint(clientConn, nextPayload)
								}
							}
						}
					}

					lastSeqNo = lastSeqNo + 1
				}
			}
		}
	}()

	eventListener, err := net.Listen("tcp", fmt.Sprintf("127.0.0.1:%d", clientPort))
	if err != nil {
		log.Fatal(err)
	}
	defer eventListener.Close()

	fmt.Printf("Listening for client requests on %d\n", clientPort)

	for {
		conn, err := eventListener.Accept()
		if err != nil {
			log.Fatal(err)
		}

		reader := bufio.NewReader(conn)

		userIDRaw, err := reader.ReadString('\n')

		if err != nil {
			log.Fatal(err)
		}

		userIDStr := strings.TrimSpace(userIDRaw)

		userID, err := strconv.Atoi(userIDStr)
		if err != nil {
			log.Fatal(err)
		}

		clientPool[userID] = conn

		fmt.Printf("User connected: %d (%d total)\n", userID, len(clientPool))
	}
}
