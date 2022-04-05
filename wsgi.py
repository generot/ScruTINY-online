from server.server import server, socket

if __name__ == "__main__":
    socket.run(server, None, 80)