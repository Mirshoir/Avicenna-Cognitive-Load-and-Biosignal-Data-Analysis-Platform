import serial.tools.list_ports

def list_available_ports():
    """List all available COM ports and descriptions."""
    ports = serial.tools.list_ports.comports()
    shimmer_ports = [port for port in ports if 'Shimmer' in port.description]
    if not shimmer_ports:
        print("No Shimmer devices detected. Ensure the device is paired and connected.")
    else:
        for port in shimmer_ports:
            print(f"Shimmer Device Port: {port.device}, Description: {port.description}")
    return [port.device for port in shimmer_ports]

ports = list_available_ports()
