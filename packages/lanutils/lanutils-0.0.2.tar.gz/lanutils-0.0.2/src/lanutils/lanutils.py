import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor

import icmplib
import ifaddr


def get_myip(
    adapters_to_find: list[str] = ["Ethernet", "Wi-Fi", "wlo1"]
) -> list[tuple[str, int, str]]:
    """Returns this machine's active local network ipv4 addresses
    for adapters listed in adapters_to_find.

    :param adapters_to_find: List of adapter names to look for
    active ip addresses. If None or an empty list, return
    any adapters with active addresses.

    Returns a list of tuples. Each tuple contains the ip address,
    network prefix, and name for the adapter."""
    myips = []
    for adapter in ifaddr.get_adapters():
        for ip in adapter.ips:
            # ipaddress module throws exception if it doesn't think the ip address is valid
            try:
                if (
                    ip.is_IPv4
                    and not ip.ip.startswith("169.254.")  # Indicates an inactive ip
                    and (
                        (adapters_to_find and ip.nice_name in adapters_to_find)
                        or not adapters_to_find
                    )
                ):
                    myips.append((ip.ip, ip.network_prefix, ip.nice_name))
            except Exception as e:
                pass
    return myips


def ip_is_alive(ip: str, timeout: float = 0.1) -> bool:
    """Checks if the host at ip is alive.

    :param timeout: How long in seconds
    to wait before declaring host dead."""
    return icmplib.ping(ip, count=1, timeout=timeout).is_alive


def enumerate_devices(timeout: float = 0.1) -> list[str]:
    """Scan the local network this device is on for devices
    and return a list of ip addresses, including this device.

    :param timeout: How long, in seconds, to wait before
    declaring an ip address inactive."""
    myip = get_myip()[0]
    network = ipaddress.ip_network(f"{myip[0]}/{myip[1]}", strict=False)
    # Skip network and broadcast ip addresses
    hosts = list(network.hosts())[1:-1]
    with ThreadPoolExecutor() as executor:
        threads = [executor.submit(ip_is_alive, str(ip), timeout) for ip in hosts]
    return [str(ip) for ip, thread in zip(hosts, threads) if thread.result()]


def port_is_open(ip: str, port: int) -> bool:
    """Returns whether a port is open on the given ip address."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    try:
        sock.connect((ip, port))
        sock.close()
        return True
    except Exception as e:
        return False


def scan_ports(ip: str, port_range: tuple[int, int] = (0, 65535)) -> list[int]:
    """Scan given ip address for open ports.

    :param port_range: Range of port numbers to scan, inclusive."""
    ports = list(range(port_range[0], port_range[1] + 1))
    with ThreadPoolExecutor() as executor:
        threads = [executor.submit(port_is_open, ip, port) for port in ports]
    return [port for port, thread in zip(ports, threads) if thread.result()]


def get_available_port(ip: str, port_range: tuple[int, int] = (0, 65535)) -> int:
    """Get the first unused port.

    :param ip: The ip address to scan.

    :param port_range: The port range to scan, bounds inclusive."""
    for port in range(port_range[0], port_range[1] + 1):
        if not port_is_open(ip, port):
            return port
    raise RuntimeError(
        f"Could not find an available port within the range {port_range}"
    )
