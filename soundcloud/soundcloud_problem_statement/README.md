**Please [read the instructions first](INSTRUCTIONS.md).**


## Running the server

### go
```
cd go
go run main.go
```

### java
```
cd java
gradle run
```

### js
```
cd js
node index.js
```

### python
Please use a modern version of python 3, managed via a tool like pyenv.
```
cd python
python main.py
```

### ruby
Please use a modern version of cruby, managed via a tool like rvm.
```
cd ruby
ruby main.rb
```

### scala
```
cd scala
sbt run
```

## About the tester

The tester makes socket connections to the server:

- The event source connects on port 9090 and will start sending events as soon as the connection is accepted. 
- The user clients can connect on port 9099,
and communicate with server following events specification and rules outlined in challenge instructions. 

## Running the tester

From the project root, run:

`tester/run100k.sh`
