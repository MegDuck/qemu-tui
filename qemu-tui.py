import os
from resources.tools.code_like_sh import clear
from resources.tools.readline_qemu import qemu_input
from resources.tools.db import *

pwd=os.getcwd()
def init() -> int:
    """
    init resources, check update
    """
    if os.path.exists("./VMs") == False:
        os.mkdir("VMs")
    
    def pwd_init(local_pwd : str):
        print("Are you want to initialize VMs directory in other locaion?(Enter if dont want) ")
        new_pwd = input(f"[{local_pwd}]: ")
        if new_pwd != "":
            if new_pwd[-1] != "/":
                new_pwd = new_pwd + "/"
            pwd = new_pwd
    

    def check_updates():
        if os.system("git>/dev/null") == 256:
            return os.system("git pull origin main>dev/null")
        else:
            print("cannot check for updates! (git not installed)")
    
    check_updates()
    pwd_init(pwd)
    clear
    return 0


def create_vm() -> int:

    """
    create vm - disk, name, preferences.

    """
    clear

    #ask for architecture(arch)
    print("choose architecture for vm(default: x86_64)")
    while True:
        arch = input("(architecture):> ")
        if arch == "":
            arch = "x86_64"
        else:
            architectures = ["aarch64", "arm", "mips", "cris", "i368", "lm32", "microblaze", "m68k", 
                             "microblazeel", "mips64el", "mips64", "mipsel", "moxie", "nios2", "or1k", 
                             "ppc", "ppc64", "ppc64el", "ppcemb", "s390x", "sh4", "sh4eb", "sparc", "sparc64"
                             "unicore32", "tricore", "x86_64", "x86_64-spice", "xtensa", "xtensaeb"]
            if arch in architectures:
                print(f"choosed: {arch}")

        print(f"You choose {arch}")
        break

    #ask for VM name
    while True:
        name = input("(name):> ")
        if name == "":
            print("VM name can't be null! ")
        else:
            break
    try:
        os.mkdir(f"VMs/{name}")
    except FileExistsError:
        print("VM with this name already created")
        return 1
    
    #ask for disk format(qcow, qcow2) and create disk with choosed memory(e.g 2GB)
    print("Size of your disk(e.g. 10GB, 5GB, 2GB) ")
    memory = ""
    while 1:
        size = input("(size_of_disk>): ")
        if size == "":
            continue
        try:
            memory = int(size.split("GB")[0])
        except ValueError:
            print("Input size of your disk not correct!")
        except IndexError:
            try:
                memory = int(size.split("TB")[0])
                
            except IndexError:
                print("Input size of your disk not correct!")
        print("qcow2 or qcow for disk(If dont know just skip by enter)")
        disk_format = input()
        if disk_format != "qcow":
            disk_format = "qcow2"
        os.system(f"cd VMs/{name} && qemu-img create -f {disk_format} {name} {memory}")
        
        #ask for RAM for VM 
        while True:
            print("RAM for your vm(default: 640)")
            ram = input("(vm_ram)> ")
            if ram == "":
                ram = 640
            try:
                ram = int(ram)
                break
            except ValueError:
                print("Input number!")
        
        #ask for iso
        print("Are you want to connect iso?(You can do it later..)[path/to/iso or Enter]")
        while True:
            path = input("( /path/to/iso ):> ")
            cpath = False
            try:
                file = open(path, "rb")
                print("Can open the iso")
                cpath = True
            except IOError as e:
                cpath = False
            if path == "":
                pass
            else:
                if cpath == True:
                    os.system(f"cd VMs/{name} && ln -s {path} {name}.iso")
                    break
                else:
                    print("not correct path!")
        
        createdb(f"./VMs/{name}/", name)
        writedb(f"./VMs/{name}/{name}.vm", "arch", arch)
        writedb(f"./VMs/{name}/{name}.vm", "acpi", "True")

        print(f"VM with name - {name} and memory {memory} created!")
        return 0

def vm_list() -> int:
    """
    Display all machines.
    """
    counter = 0
    try:
        for i in os.listdir("./VMs"):
            print(f"[{counter}]: {i}")
            counter += 1
    except FileNotFoundError:
        print("can't find ./VMs dir!")
        return 1
    return 0

def run_vm(vm_name : str) -> None:
    if vm_name in os.listdir("./VMs/"):
        print(f"{vm_name} found..")
    else:
        print(f"Cannot find vm with name {vm_name}")
        return 1

    usb = False
    command = "qemu-system-"
    #add architecture to command
    arch = readdb(f"./VMs/{vm_name}/{vm_name}.vm")["arch"]
    command = command + arch
    #add hda to command
    command = command + f" -hda ./VMs/{vm_name}/{vm_name}"


    #check for iso and if iso found in dir add to command -cdrom 
    if f"{vm_name}.iso" in os.listdir(f"./VMs/{vm_name}/"):
        usb = True
        print("iso found..")
    if usb == True:
        command = command + f" -cdrom ./VMs/{vm_name}/{vm_name}.iso"
    command = command + " -m 1280"
    os.system(command)


def display_menu() -> None:
    """
    display your machines and little help about.
    """
    clear
    print(open(f"{pwd}/resources/motd").read())
    print("Your VMs: ")
    vm_list()
    print()
    while True:
        try:
            stdin = qemu_input(promt="(>): ", histfile=".histfile")
            if stdin.lower().split()[0] == "create" or stdin.lower().split()[0] == "c":
                create_vm()

            elif stdin.lower().split(" ")[0] in ["env"]:
                vm_name = ""
                try:
                    vm_name = stdin.split(" ")[1]
                except IndexError:
                    print("incorrect use: env <VM name>")
                    pass
                if os.path.exists(f"./VMs/{vm_name}"):
                    print(f"┌{vm_name}")
                    for i in os.listdir(f"./VMs/{vm_name}/"):
                        if os.path.islink(f"./VMs/{vm_name}/{i}"):
                            print(f"─ @{i}")
                        else:
                            print(f"─ {i}")
                        
            elif stdin.lower().split()[0] == "exit" or stdin.lower().split()[0] == "e":
                    break

            elif stdin.lower().split(" ")[0] in ["remove", "rm"]:
                vm_name = ""
                try:
                    vm_name = stdin.lower().split(" ")[1]
                    try:
                        #if iso find in ./VMs/*virtual_machine_name* unlink it. 
                        if f"{vm_name}.iso" in os.listdir(f"./VMs/{vm_name}"):
                            os.unlink(f"./VMs/{vm_name}/{vm_name}.iso")
                            print(f"unlink {vm_name}.iso...")

                        #remove directory with content of VM
                        from shutil import rmtree
                        rmtree(f"./VMs/{vm_name}", ignore_errors=True)
                        print("Remove succesfly!")
                    except FileNotFoundError:
                        print("No VM with this name!")
                except IndexError:
                    print("Incorrect use: remove <VM Name>")

            elif stdin.lower().split(" ")[0] in ["r", "run"]:
                try:
                    vm_name = stdin.split()[1]
                    run_vm(vm_name)
                except IndexError:
                    print("incorrect use: run <VM_name>")

            elif stdin.lower() in ["list", "l"]:
                vm_list()
        except IndexError:
            pass

def main():
    init()
    display_menu()


main()