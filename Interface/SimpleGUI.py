import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

class STM32ControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STM32 Control")

        # Serial port selection
        self.port_var = tk.StringVar()
        self.port_dropdown = ttk.Combobox(root, textvariable=self.port_var)
        self.port_dropdown['values'] = self.get_serial_ports()
        self.port_dropdown.state(['readonly'])
        self.port_dropdown.pack(pady=10)

        # Connect button
        self.connect_button = tk.Button(root, text="Connect", command=self.connect)
        self.connect_button.pack(pady=10)

        # Start button
        self.start_button = tk.Button(root, text="Start Operation", command=self.send_start_signal, state=tk.DISABLED)
        self.start_button.pack(pady=10)

        # Stop button
        self.stop_button = tk.Button(root, text="Stop Operation", command=self.send_stop_signal, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Close button
        self.close_button = tk.Button(root, text="Close", command=self.close)
        self.close_button.pack(pady=10)

        self.serial_connection = None

    def get_serial_ports(self):
        """List all available serial ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self):
        """Connect to the selected serial port."""
        port = self.port_var.get()
        if port:
            try:
                self.serial_connection = serial.Serial(port, 115200, timeout=1)
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.NORMAL)
                print(f"Connected to {port}")
            except serial.SerialException as e:
                print(f"Failed to connect to {port}: {e}")

    def send_start_signal(self):
        """Send the START command to the STM32."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write(b'START\n')
            print("Start signal sent")

    def send_stop_signal(self):
        """Send the STOP command to the STM32."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write(b'STOP\n')
            print("Stop signal sent")

    def close(self):
        """Close the serial connection and the application."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = STM32ControlApp(root)
    root.mainloop()
