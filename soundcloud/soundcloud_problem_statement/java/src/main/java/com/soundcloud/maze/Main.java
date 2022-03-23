package com.soundcloud.maze;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

import static java.util.Collections.emptySet;

public class Main {

    private final static int EVENT_PORT = 9090;
    private final static int CLIENT_PORT = 9099;

    private static long lastSeqNo = 0L;

    public static void main(String[] args) {

        Map<Long, Socket> clientPool = new ConcurrentHashMap<>();
        Map<Long, List<String>> seqNoToMessage = new HashMap<>();

        Map<Long, Set<Long>> followRegistry = new HashMap<>();

        new Thread(() -> {
            System.out.println("Listening for events on " + EVENT_PORT);
            try (Socket eventSocket = new ServerSocket(EVENT_PORT).accept()) {
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(eventSocket.getInputStream()))) {
                    reader.lines().forEach(payload -> {
                        System.out.println("Message received: " + payload);

                        List<String> payloadParts = Arrays.asList(payload.split("\\|"));
                        seqNoToMessage.put(Long.parseLong(payloadParts.get(0)), payloadParts);

                        while (seqNoToMessage.containsKey(lastSeqNo + 1)) {
                            List<String> nextMessage = seqNoToMessage.get(lastSeqNo + 1);
                            String nextPayload = String.join("|", nextMessage);

                            long seqNo = Long.parseLong(nextMessage.get(0));
                            String kind = nextMessage.get(1);

                            switch (kind) {
                                case "F": {
                                    long fromUserId = Long.parseLong(nextMessage.get(2));
                                    long toUserId = Long.parseLong(nextMessage.get(3));

                                    Set<Long> followers = followRegistry.getOrDefault(toUserId, new HashSet<>());
                                    followers.add(fromUserId);
                                    followRegistry.put(toUserId, followers);

                                    try {
                                        Socket socket = clientPool.get(toUserId);
                                        if (socket != null) {
                                            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
                                            writer.write(nextPayload + "\n");
                                            writer.flush();
                                        }
                                    } catch (IOException e) {
                                        throw new RuntimeException(e);
                                    }
                                }
                                break;

                                case "U": {
                                    long fromUserId = Long.parseLong(nextMessage.get(2));
                                    long toUserId = Long.parseLong(nextMessage.get(3));

                                    Set<Long> followers = followRegistry.getOrDefault(toUserId, new HashSet<>());
                                    followers.remove(fromUserId);
                                    followRegistry.put(toUserId, followers);
                                }
                                break;

                                case "P": {
                                    long toUserId = Long.parseLong(nextMessage.get(3));

                                    try {
                                        Socket socket = clientPool.get(toUserId);
                                        if (socket != null) {
                                            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
                                            writer.write(nextPayload + "\n");
                                            writer.flush();
                                        }
                                    } catch (IOException e) {
                                        throw new RuntimeException(e);
                                    }
                                }
                                break;

                                case "B": {
                                    clientPool.values().forEach(socket -> {
                                        try {
                                            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
                                            writer.write(nextPayload + "\n");
                                            writer.flush();
                                        } catch (IOException e) {
                                            throw new RuntimeException(e);
                                        }
                                    });
                                }
                                break;

                                case "S": {
                                    long fromUserId = Long.parseLong(nextMessage.get(2));

                                    Set<Long> followers = followRegistry.getOrDefault(fromUserId, emptySet());

                                    followers.forEach(follower -> {
                                        try {
                                            Socket socket = clientPool.get(follower);
                                            if (socket != null) {
                                                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
                                                writer.write(nextPayload + "\n");
                                                writer.flush();
                                            }
                                        } catch (IOException e) {
                                            throw new RuntimeException(e);
                                        }
                                    });
                                }
                                break;
                            }

                            lastSeqNo = seqNo;
                        }
                    });
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }).start();

        new Thread(() -> {
            System.out.println("Listening for client requests on " + CLIENT_PORT);
            try {
                ServerSocket serverSocket = new ServerSocket(CLIENT_PORT);
                Socket clientSocket = serverSocket.accept();
                while (clientSocket != null) {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                    String userId = reader.readLine();
                    if (userId != null) {
                        clientPool.put(Long.parseLong(userId), clientSocket);
                        System.out.println("User connected: " + userId + " (" + clientPool.size() + " total)");
                    }
                    clientSocket = serverSocket.accept();
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }).start();

    }
}
