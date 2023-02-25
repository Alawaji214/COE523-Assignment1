
# Assignment 1

Group 1

## Objective

In this assignment, you will learn:

* Implementing client/server communication through python sockets
* Programming multi-threaded server to handle multiple clients’ requests
* Implementing process/thread synchronization in python

## Problem Statement

You are required to produce two programs, chatserver and chatclient. There can be more than
one instances of chatclient running at a time and the purpose of chatserver is to provide a link
between all the available clients so that they can talk to each other.

### Requirements

### chatserver

### chatclient

### message

### Standard/Control Message Formats

### CheckLists

#### Server

- [ ] Receiving Message from client (includes tokenization of message): 5
- [ ] Forward/Reply Message to client (includes creation of message in specified format): 5
- [ ] Creating Client List: 5
- [ ] Sending Client List: 5
- [ ] Adding new Client to List: 5
- [ ] Deleting Client from List: 5
- [ ] Retiring Client: 5
- [ ] Informing about change in List: 5
- [ ] Reply Message if message for offline Client: 5
- [ ] Resetting Client life on receiving alive message: 5

#### Client

- [ ] Exchange Messages with another clients via server: 10
- [ ] Receiving client list from server (includes tokenization of message): 10
- [ ] Sending Message to server (includes creation of message in specified format): 10
- [ ] Displaying Client List: 5
- [ ] Sending alive message: 5
- [ ] Sending connect message: 5
- [ ] Sending quit message: 5