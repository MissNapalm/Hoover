import platform
import psutil
import json
import socket
import GPUtil
import wmi

def format_bytes(size):
    # Convert bytes to a human-readable format
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

def get_motherboard_info():
    motherboard_info = {}

    # Windows-specific code
    if platform.system() == 'Windows':
        try:
            c = wmi.WMI()
            motherboard_info['Manufacturer'] = c.Win32_BaseBoard()[0].Manufacturer
            motherboard_info['Product'] = c.Win32_BaseBoard()[0].Product
            motherboard_info['BIOS Version'] = c.Win32_BIOS()[0].Version
            motherboard_info['BIOS Release Date'] = c.Win32_BIOS()[0].ReleaseDate
        except ImportError:
            pass

    return motherboard_info

def get_system_info():
    system_info = []

    # OS information
    os_info = [
        ("System", platform.system()),
        ("Version", platform.version()),
        ("Architecture", platform.architecture()),
        ("Machine", platform.machine())
    ]
    system_info.append(("OS Information", os_info))

    # CPU information
    processor = platform.processor()
    cpu_info = [
        ("Processor", processor if processor else "N/A"),
        ("Architecture", platform.architecture()),
        ("Cores", psutil.cpu_count(logical=False)),
        ("Logical CPUs", psutil.cpu_count(logical=True)),
        ("CPU Usage", psutil.cpu_percent(interval=1, percpu=True)),
        ("Clock Speed", psutil.cpu_freq().current)
    ]
    system_info.append(("CPU Information", cpu_info))

    # RAM information
    ram_info = [
        ("Total RAM", format_bytes(psutil.virtual_memory().total)),
        ("Available RAM", format_bytes(psutil.virtual_memory().available)),
        ("Used RAM", format_bytes(psutil.virtual_memory().used)),
        ("RAM Usage Percentage", f"{psutil.virtual_memory().percent}%")
    ]
    system_info.append(("RAM Information", ram_info))

    # Motherboard information
    motherboard_info = get_motherboard_info()
    if motherboard_info:
        system_info.append(("Motherboard Information", list(motherboard_info.items())))
    else:
        system_info.append(("Motherboard Information", "Motherboard information not available."))

    # Hard drive information
    hard_drive_info = []
    partitions = psutil.disk_partitions(all=False)
    for partition in partitions:
        partition_info = [
            ("Device", partition.device),
            ("Mount Point", partition.mountpoint),
            ("File System", partition.fstype),
            ("Total Size", format_bytes(psutil.disk_usage(partition.mountpoint).total)),
            ("Used Space", format_bytes(psutil.disk_usage(partition.mountpoint).used)),
            ("Free Space", format_bytes(psutil.disk_usage(partition.mountpoint).free)),
            ("Usage Percentage", f"{psutil.disk_usage(partition.mountpoint).percent}%")
        ]
        hard_drive_info.append(("Partition Information", partition_info))
    system_info.append(("Hard Drive Information", hard_drive_info))

    # Network statistics
    network_info = [
        ("Hostname", socket.gethostname()),
        ("IP Address", socket.gethostbyname(socket.gethostname())),
        ("Network Speed", psutil.net_if_stats())
    ]
    system_info.append(("Network Information", network_info))

    # GPU information
    try:
        gpu_info = []
        gpus = GPUtil.getGPUs()
        for i, gpu in enumerate(gpus):
            gpu_info.append([
                ("GPU Name", gpu.name),
                ("GPU Driver", gpu.driver),
                ("GPU Memory Total", format_bytes(gpu.memoryTotal)),
                ("GPU Memory Free", format_bytes(gpu.memoryFree)),
                ("GPU Memory Used", format_bytes(gpu.memoryUsed)),
                ("GPU Usage Percentage", f"{gpu.load * 100}%"),
                ("GPU Temperature", f"{gpu.temperature}°C")
            ])
    except GPUtil.GPUtilError:
        gpu_info = "GPU information not available."
    system_info.append(("GPU Information", gpu_info))

    return system_info

def get_usb_devices_info():
    usb_devices_info = []

    try:
        # Iterate over USB devices
        for device in psutil.disk_partitions(all=False):
            if 'removable' in device.opts:
                usb_device_info = [
                    ("Device", device.device),
                    ("Mount Point", device.mountpoint),
                    ("File System", device.fstype),
                    ("Total Size", format_bytes(psutil.disk_usage(device.mountpoint).total)),
                    ("Used Space", format_bytes(psutil.disk_usage(device.mountpoint).used)),
                    ("Free Space", format_bytes(psutil.disk_usage(device.mountpoint).free)),
                    ("Usage Percentage", f"{psutil.disk_usage(device.mountpoint).percent}%")
                ]
                usb_devices_info.append(("USB Device Information", usb_device_info))
    except Exception as e:
        print(f"Error retrieving USB device information: {e}")

    return usb_devices_info

def format_seconds(seconds):
    # Convert seconds to a human-readable format (days, hours, minutes, seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"

def main():
    # Display ASCII art for "Hoover"
    hoover_art = """
                                  ▓▓██████████████████████████████▓▓                                              
                              ▒▒██                                  ██▒▒                                          
                              ██    ██████████████████████████████░░  ██▒▒                                        
                            ▓▓░░  ██                              ██    ██░░                                      
                            ██  ▓▓                                  ██    ██                                      
                            ██  ▓▓                                    ██░░  ██                                    
                            ██  ██                                      ▓▓░░  ██                                  
                            ██  ▒▒▓▓                                      ██  ██                                  
                              ▓▓  ▓▓██▓▓████████████████▓▓                ██  ██                                  
                              ▓▓██                      ▒▒██              ██  ██                                  
                                  ▓▓████████████████████▒▒  ██            ██  ██                                  
                                    ░░░░░░░░░░░░░░░░░░░░██░░░░▓▓          ██  ██                                  
                                                          ██  ██          ██  ██                                  
                                                          ▓▓  ██          ██  ██                                  
                                                          ▒▒  ██          ██  ██                                  
                                                          ██  ██          ██  ██                                  
                                                          ▓▓  ▒▒          ██  ██                                  
                                  ▓▓▓▓▓▓██▒▒            ██  ██            ██  ██                                  
                                ▓▓░░      ░░██▓▓██      ██  ██            ██  ██                                  
                                ▓▓              ████    ▓▓  ▓▓            ██  ██                                  
                                ██                  ▓▓▓▓  ▓▓              ██  ██                                  
                                ██                    ▒▒▓▓██              ██  ██                                  
                                ██                      ▒▒▓▓              ██  ██                                  
                                ██████▒▒                  ▓▓░░            ██  ██                                  
                              ████    ▒▒██                  ██            ██  ██                                  
                            ▓▓          ░░▓▓                ▓▓          ██████████                                
                            ██            ██                ░░▒▒        ██      ██                                
                            ██            ██  ▓▓▓▓▓▓▓▓▒▒▓▓    ▓▓        ██      ██                                
                            ██            ██                  ██    ▓▓████      ████▓▓                            
                            ▓▓            ▓▓  ████████████    ██  ██                  ██                          
                              ██        ██                    ██  ██                  ██                          
                              ▒▒██▓▓▓▓████▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒░░██▒▒  ██▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒██  HOOVER V. 1.03        
    """

    print(hoover_art)
    input("This program will gather a large amount of information on your computer. Press enter to continue.")

    system_info = get_system_info()

    # Print information on screen
    print("System Information:")
    for section_name, section_info in system_info:
        print(f"\n{section_name}:")
        if isinstance(section_info, list):
            for item in section_info:
                if isinstance(item, tuple):
                    print(f"  {item[0]}: {item[1]}")
                elif isinstance(item, list):
                    print(f"  {item[0]}:")
                    for subitem in item[1]:
                        print(f"    {subitem[0]}: {subitem[1]}")
        else:
            print(f"  {section_info}")

    # Prompt user to save general system info to JSON
    save_system_info = input("\nSave these results to a JSON? (Y/N): ").strip().lower()
    if save_system_info == 'y':
        with open('system_info.json', 'w') as json_file:
            json.dump(dict(system_info), json_file, indent=4)
            print("System information saved to 'system_info.json'.")

    # Prompt user to save running processes to JSON
    save_processes = input("\nSave current running processes to a JSON? (Y/N): ").strip().lower()
    if save_processes == 'y':
        processes = [{'pid': process.pid, 'name': process.name()} for process in psutil.process_iter(['pid', 'name'])]
        with open('running_processes.json', 'w') as json_file:
            json.dump(processes, json_file, indent=4)
            print("Running processes saved to 'running_processes.json'.")

    # Prompt user to save network ports info to JSON
    save_network_ports = input("\nSave info on network ports? (Y/N): ").strip().lower()
    if save_network_ports == 'y':
        network_ports = psutil.net_connections(kind='inet')
        network_ports_info = [{'local_address': conn.laddr, 'remote_address': conn.raddr, 'status': conn.status} for conn in network_ports]
        with open('network_ports.json', 'w') as json_file:
            json.dump(network_ports_info, json_file, indent=4)
            print("Network ports info saved to 'network_ports.json'.")

    # Prompt user to save connected USB devices info to JSON
    save_usb_devices = input("\nSave connected USB device information? (Y/N): ").strip().lower()
    if save_usb_devices == 'y':
        usb_devices_info = get_usb_devices_info()
        with open('usb_devices_info.json', 'w') as json_file:
            json.dump(dict(usb_devices_info), json_file, indent=4)
            print("USB device information saved to 'usb_devices_info.json'.")

if __name__ == "__main__":
    main()
