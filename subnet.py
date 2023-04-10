#!/usr/bin/python3 

from prettytable import PrettyTable
import sys

class Colors:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"


if len(sys.argv) != 2:
    print(f"\n{Colors.YELLOW}[+] Example : {Colors.END} {Colors.BLUE}python3 {Colors.END}" + sys.argv[0] + f"{Colors.RED} 192.168.1.1/24{Colors.END}\n")
    sys.exit(1)

# User Input
host_cidr = sys.argv[1]

if "/" not in host_cidr:
    print(f"\n\n{Colors.YELLOW} [!]{Colors.END} {Colors.RED} Invalid host {Colors.END}\n")
    sys.exit(1)

# Split User INPUT    
host = host_cidr.split("/")[0]
cidr = host_cidr.split("/")[1]

if cidr == "0" or int(cidr) > 32:
    print(f"\n\n{Colors.YELLOW}[!]{Colors.END} {Colors.RED}Invalid CIDR{Colors.END}\n")
    sys.exit(1)

elif len(host.split(".")) > 4:
    print(f"\n\n{Colors.YELLOW} [!]{Colors.END} {Colors.RED} Invalid host {Colors.END}\n")
    sys.exit(1)


def binary_ip(host):
    try:
        binary_list = list()
        final_number = ""

        for i in host.split("."):
            binary_number = bin(int(i)).replace("0b","")
            while len(binary_number) < 8:
                binary_number = binary_number[::-1] + "0"
                binary_number = binary_number[::-1]
            
            final_number += binary_number
        
        for k in final_number:
            binary_list.append(k)

        return binary_list

    except Exception as error:
        log.error(str(error))
        
def binary_mask(cidr):
    try:
        mask_list = list()
        cidr = int(cidr)
        for i in range(cidr):
            part_net = "1" * cidr
            part_host = "0" * (32 - cidr)
            total_bits = part_net + part_host

        for j in total_bits:
            mask_list.append(j)
        
        return mask_list

    except Exception as error:
        log.error(str(error))
        
def network_id(binary_list,mask_list):
    decimal_list = []
    result = []
    for x,y in zip(binary_list,mask_list):
        result.append(int(bool(int(x))) and int(bool(int(y))))
    
    chain = "".join(str(num) for num in result) 
    
    for number in range(0,len(chain),8):
        div_num = chain[number:number+8]
        decimal_list.append(int(div_num,2))

    first_ip = ".".join(str(num) for num in decimal_list)

    return first_ip

def get_mask(mask_list):
    value = "".join(str(i) for i in mask_list)
    net_list = []
    
    for k in range(0,len(value),8):
        net_value = value[k:k+8]
        net_list.append(int(net_value,2))
        
    string_mask = "%d.%d.%d.%d" % (net_list[0],net_list[1],net_list[2],net_list[3])

    return string_mask

def get_last_ip(binary_ip,mask_list):
    result = []
    binary_ip[int(cidr):] = [1] * (len(binary_ip) - int(cidr))
     
    broadcast_chain = "".join(map(str,binary_ip))
    new_chain = ".".join(broadcast_chain[i:i+8] for i in range(0,len(binary_ip),8))
    
    final_list = new_chain.split(".")

    for decimal_number in final_list:
        result.append(int(decimal_number,2))

    value = ".".join(str(numbers) for numbers in result) 

    return value 

if __name__ == '__main__':
    binary_list = binary_ip(host)
    mask_list = binary_mask(cidr)

    first_ip = network_id(binary_list,mask_list)
    mask_value = get_mask(mask_list)
    last_ip = get_last_ip(binary_list,mask_list)

    table = PrettyTable()
    table.field_names = [f"{Colors.RED}Information{Colors.END}", f"{Colors.RED}Value{Colors.END}"]
    table.add_row([f"{Colors.YELLOW}First IP{Colors.END}", f"{Colors.BLUE}" + first_ip + f"{Colors.END}"])
    table.add_row([f"{Colors.YELLOW}Last IP{Colors.END}", f"{Colors.BLUE}" + last_ip + f"{Colors.END}"])
    table.add_row([f"{Colors.YELLOW}Netmask{Colors.END}", f"{Colors.BLUE}" +  str(mask_value) + f"{Colors.END}"])
    table.add_row([f"{Colors.YELLOW}Total Hosts{Colors.END}", f"{Colors.BLUE}" + str(2**(32 - int(cidr))) + f"{Colors.END}" ])

    print(table)
