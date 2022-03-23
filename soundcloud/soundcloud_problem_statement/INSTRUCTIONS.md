# Follower Maze Code Challenge Instructions

Thank you for applying for a backend engineering position at SoundCloud. 
We ask engineering candidates to work and complete this code challenge. 
Your submission is part of the basis upon which we evaluate your candidacy.

We hope it’s indeed challenging (and maybe even fun).

The challenge has two parts:
1. **Refactor** an existing client-server application and provide a README explaining your approach
1. **Extend** the server application with a small feature request

Our aim with these instructions is to leave no doubt about the details of the challenge and the expectations of 
your submission - however, if you have questions of any sort _please ask_. 
Also: please completely read the instructions before starting!

## Time Expectations

Based on internal testing, we roughly estimate the full Follower-Maze challenge will take 
somewhere around 2-7 hours of your time.
 
* Our goal for this time budget is to keep the time investment predictable for candidates - 
it is not intended to create significant “time pressure”. 
* The length of time you take to submit your work is not a factor in how we review it.
* Many candidates will work the challenge and submit it back within a day or two. 
Or some might submit it a week later, depending on personal circumstances.

## Discretion
In order to ensure continued fairness to all past and future participants, 
please do not share any of the details of this code challenge with others, 
including the work you submit.

## Anonymity
Code challenge submissions are treated as a form of [Blind Audition](https://en.wikipedia.org/wiki/Blind_audition): 
reviewers don’t have access to a candidate’s personal information, 
including name and background. 
Please help us by keeping your submission free of information 
that would be revealing of who you are, or any personal attributes.

## Part 1: Follower Maze - Refactor

### Overview

Follower-Maze is a **client-server application** built for social networking. 
Users follow other users, post messages, send private messages, unfollow users, and so on. 
* Each of these actions is an _event_, created by an _event-source_ and sent to the _server_.
* Each event is processed by the _server_.
* The processing of the event may have follow-on effects on other _user-clients_.

The **server** listens for two kinds of **clients**:
* **1 event source**, which emits events.
* **N user-clients** that connect to the server.

The server routes certain events to certain clients, according to the social networking domain rules. 
Please see the [Specification](#specification) section for more detail.

### Running the End-to-End Tester

Please see the repository [README](README.md) for instructions on how to run client/server implementations, 
and the end-to-end tester.


You have the choice of one of six programming language implementations: 
please choose the language you’re most comfortable in, 
and try running the client/server implementation for that language, 
and then run the end-to-end tester to successful completion.

### Specification

This specification is just for your reference. 
The provided implementations are based on this specification.


#### Client/Server Protocol

* The protocol is line-based i.e. a LF control character terminates each message. 
All strings are encoded in UTF-8.
* Data is transmitted over TCP sockets.
* The _event source_ connects on port 9090 and will start sending events as soon as the connection is accepted.
* The _user clients_ connect on port 9099 and identify themselves with their user ID. 
For example, once connected a _user client_ may send down `2932\r\n`, 
indicating that it is representing user 2932.
* After the identification is sent, 
the user client starts waiting for events to be sent to them by the server.

#### Events

There are five possible events. 
The table below describes payloads sent by the event source and what each represents:

```
| Payload       | Sequence # | Type          | From User Id | To User Id |
|---------------|------------|---------------|--------------|------------|
| 666|F|60|50   | 666        | Follow        | 60           | 50         |
| 1|U|12|9      | 1          | Unfollow      | 12           | 9          |
| 542532|B      | 542532     | Broadcast     | -            | -          |
| 43|P|32|56    | 43         | Private Msg   | 32           | 56         |
| 634|S|32      | 634        | Status Update | 32           | -          |
```

#### Event Rules

* Each message begins with a sequence number.
* However, the event source _does not send events in any given order_. 
In particular, sequence number has no effect on the order in which events are sent.
* Events _may_ generate notifications for _user clients_. 
If there is a respective target _user client_ connected, 
the notification is routed according to the following rules:
  * Follow: Only the `To User Id` is notified
    * A follow event from user A to user B means that user A now follows user B.
  * Unfollow: No clients are notified
    * An unfollow event from user A to user B means that user A stopped following user B.
  * Broadcast: All connected _user clients_ are notified
  * Private Message: Only the `To User Id` is notified
  * Status Update: All current followers of the `From User ID` are notified
* If there are no _user clients_ connected for a user, 
any notifications for them are currently ignored. 
_User clients_ are notified of events _in the correct sequence-number order_, 
regardless of the order in which the _event source_ sent them.

### Challenge
We have provided the client and server code - this is your starting point. 
However, the code is in poor shape: 
it’s condensed into giant blocks of code in a single file, 
making it hard for you to understand, debug, and test. 
**Your task is to refactor the code so that it’s _easy to test, 
easy to understand and easy to maintain._**

### Guidance

**Time budget:** We roughly estimate this portion will take between 2-6 hours.

The **primary goals** of this exercise are:
* To provide structure and clarity to the server code base by introducing appropriate abstractions.
* To produce code that accommodates change and is easy to test.
* To maintain correctness of the server program.
* To document your approach.

Some **non-goals**:
* To introduce functionality that was not asked for.
* To make the solution production-ready. 
  * **HOWEVER** we ARE interested in what top improvements you think need to be made 
  to make it production-ready (see README details below).
* To write unit tests; your focus should be on writing testable code first, 
and while you're free to write unit tests with this part of the exercise, 
it is not a stated requirement here.

## Part 2: Follower Maze - Extension

### The Problem

In Part 1, we asked you to refactor an existing solution to the follower-maze problem. 
The original specification of the problem leaves the question of bad event data unanswered, 
and it simplifies the case of undeliverable notifications in case of user disconnects. 
Your task is to **add a [Dead Letter Queue (DLQ)](https://en.wikipedia.org/wiki/Dead_letter_queue)
to the server**, so that undeliverable or malformed messages aren't lost. 

“Dead letters” build up and ultimately must be dealt with. 
For the purposes of this interview problem, 
it's OK to simply log them to the console. 
But please **include a short explanation in your README** of how you would store and process 
that data in a production scenario.


### Guidance

**Time budget:** We roughly estimate this portion will take between 1-2 hours.

The **primary goals** of this exercise are:
* To introduce a DLQ implementation
* To capture messages that fall outside of the original specification of the protocol, for example:
  * Malformed messages
  * New message types not yet supported by the server
* To capture messages that cannot be delivered because the target user is not connected
* To write unit tests demonstrating the DLQ operates as specified
* To explain your approach to handling “dead letters” in production, in your README

Some **non-goals**:

* To introduce functionality or improvements that were not asked for
* To make the solution production-ready 
(but you're welcome to comment on that aspect in your README file)

## Constraints

* Pick one of the six programming languages, 
and base your solution on that language’s initial implementation.
* Please restrict yourself to the standard library - don’t introduce 3rd party libraries. 
**Exception:** libraries that facilitate unit testing are acceptable. 

## Deliverables

### Deliverables For Part 1

* Your refactored version of the code.
* A README file detailing:
  * The approach you took and reasoning you applied to arrive at your final solution.
  * Explanation of any design trade-offs or short-cuts you may have taken.
  * How to run the server, in case you made changes to the setup we provided.
  * The top priorities you would have for additions or modifications to make the solution production-ready.
  
_Remember: unit tests are not required for Part 1_

### Deliverables For Part 2
* A working implementation of a DLQ that handles messages falling into the categories specified above.
* Unit tests demonstrating the newly added functionality is working as specified.
* In your README:
  * The approach you took and reasoning you applied to arrive at your final solution; 
pay particular attention to design trade-offs or short-cuts you may have taken.
  * Explanation of what more you would do with DLQ messages in a production scenario
(i.e. aside from simply logging them to the console).

## Tips
* Run the end-to-end tester regularly as you change code.
* We're looking for a simple, straight-forward, clean & concise solution. 
* If you have technical questions, please ask!


