# Follower Maze Code Challenge Instructions

Follower-Maze is a **client-server application** built for social networking. 
Users follow other users, post messages, send private messages, unfollow users, and so on. 
* Each of these actions is an _event_, created by an _event-source_ and sent to the _server_.
* Each event is processed by the _server_.
* The processing of the event may have follow-on effects on other _user-clients_.

The **server** listens for two kinds of **clients**:
* **1 event source**, which emits events.
* **N user-clients** that connect to the server.


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



