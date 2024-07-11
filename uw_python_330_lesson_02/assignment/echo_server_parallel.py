import socket
import sys
import traceback
import select
import time

MSG_SIZE = 16


class Connection():
    def __init__(self, conn, addr, conn_type):
        self.conn = conn
        self.conn_type = conn_type
        self.addr = addr
        self.chunk = None

    def receive_message(self):
        self.chunk = self.conn.recv(MSG_SIZE)
        print('received "{0}"'.format(self.chunk.decode('utf8')))
        self.conn_type = "write"
        if len(self.chunk) < MSG_SIZE:
            print(
                'echo complete, client connection closed'
            )
            self.send_message()
            self.close_connection()

    def send_message(self):
        self.conn.sendall(self.chunk)
        print('sent "{0}"'.format(self.chunk.decode('utf8')))
        self.conn_type = "read"

    def close_connection(self):
        self.conn_type = "finished"
        self.conn.close()

    def fileno(self):
        return self.conn.fileno()


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    # set up server
    server = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    # set so it will wait for port
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    # bind server to ip
    server.bind(address)
    server.listen(5)
    try:
        # set up initial connections with the server
        server_connection = Connection(server, address, "read")
        connections = [server_connection]
        while True:
            print('waiting for a connection', file=log_buffer)
            # clean list
            connections = [
                conn for conn in connections if conn.conn.fileno() != -1]
            # sort into read and write connections
            read_connections = [
                conn for conn in connections if conn.conn_type == "read"]
            write_connections = [
                conn for conn in connections if conn.conn_type == "write"]
            # get lists that are ready
            ready_to_read, ready_to_write, in_error = \
                select.select(
                    read_connections,
                    write_connections,
                    [],
                    30)
            # *** USE THIS TO TEST MULTIPLE CLIENTS ***
            # time.sleep(10)
            try:
                for conn in ready_to_read:
                    if conn is server_connection:
                        conn, addr = server.accept()
                        print('connection - {0}:{1}'.format(*addr))
                        connections.append(Connection(conn, addr, "read"))
                    else:
                        conn.receive_message()
                for conn in ready_to_write:
                    conn.send_message()
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)

    except KeyboardInterrupt:
        # TODO: Use the python KeyboardInterrupt exception as a signal to
        #       close the server socket and exit from the server function.
        #       Replace the call to `pass` below, which is only there to
        #       prevent syntax problems
        print('quitting echo server', file=log_buffer)
        for conn in connections:
            conn.close_connection()

    except TimeoutError:
        # timeout if connectiont takes too long. for some reason keyboard interupt was
        # not working for me so this is a failsafe
        print('client took too long to connect. quitting echo server', file=log_buffer)
        if server:
            server.close()


if __name__ == '__main__':
    server()
    sys.exit(0)
