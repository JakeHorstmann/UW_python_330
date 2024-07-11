import socket
import time


def used_ports(lower_bound="4000", upper_bound="5000"):
    """
    Check what ports are being used between the lower
    and upper bound
    """
    # check if input are integers
    if not (lower_bound.isnumeric() and upper_bound.isnumeric()):
        print("Lower and upper bound must be integers")
        return None
    lower_bound = int(lower_bound)
    upper_bound = int(upper_bound)
    # check is values are in valid port range
    if not ((0 <= lower_bound <= 65535) and (0 <= upper_bound <= 65535)):
        print("Lower and upper bound must be between 0 and 65535")
        return None
    # check if they make sense
    if (upper_bound - lower_bound) < 0:
        print("Upper bound must be greater than lower bound")
        return None
    # scan ports between range
    open_ports = []
    start_time = time.time()
    try:
        for port in range(lower_bound, upper_bound+1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                              socket.IPPROTO_TCP)
            s.settimeout(.1)
            address = ('localhost', port)
            response = s.connect_ex(address)
            if response == 0:
                open_ports.append(port)
            s.close()
        end_time = time.time()
        diff = end_time - start_time
        print(f"Scan took {diff} seconds")
        print(f"Average port scan took {diff/(upper_bound-lower_bound+1)}")
        for port in open_ports:
            print(f"Port {port} is available on this computer")
        return open_ports
    except:
        print("Scan errored out. Quitting...")
        return


if __name__ == "__main__":
    lower_bound = input("Enter a lower port bound: ")
    upper_bound = input("Enter an upper port bound: ")
    used_ports(lower_bound, upper_bound)
