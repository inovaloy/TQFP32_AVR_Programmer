import os
import argparse
import sys
import subprocess
import re

FIRMWARE_BUILD           = "build"
FIRMWARE_FLASH           = "flash"
CONTROLLER_DETECT        = "detect"

ATMEGA8A_SIGNATURE       = "0x1e9307"
ATMEGA328PU_SIGNATURE    = "0x1e950f"
ATMEGA328PB_SIGNATURE    = "0x1e9516"

ATMEGA8A_NAME_STRING     = "Atmega8A"
ATMEGA328PU_NAME_STRING  = "Atmega328PU"
ATMEGA328PB_NAME_STRING  = "Atmega328PB"

class Builder:
    def __init__(self, mode):
        self.mode = mode

        if self.mode == FIRMWARE_BUILD:
            print("Firmware Build start")

        if self.mode == FIRMWARE_FLASH:
            print("Firmware Flash start")

        if self.mode == CONTROLLER_DETECT:
            self.controllerDetection()


    def executeCommand(self):
        log = []
        base_arg = ["sudo", "avrdude", "-v",
                "-C", "avrdude.conf",
                "-p", "1200",
                "-c", "linuxgpio"]
        process = subprocess.Popen(base_arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while process.poll() is None:
            line = process.stderr.readline().strip()
            if line != b'':
                log.append(str(line))

        exitCode = process.wait()
        return exitCode, log


    def controllerDetection(self):
        print("Controller Detection start")
        exitCode, log = self.executeCommand()
        signatureFound = False
        for logLine in log:
            if "Device signature" in logLine:
                signatureFound = True
                signature = re.findall("(0[xX][0-9a-fA-F]+)", logLine)[0]
                if int(signature, 16) != 0:
                    print("Signature:", signature)
                    break

        if signatureFound and int(signature, 16) == 0:
            print("Null Signature")
            return

        if signatureFound:
            if signature == ATMEGA8A_SIGNATURE:
                print("Controller:", ATMEGA8A_NAME_STRING)
            elif signature == ATMEGA328PU_SIGNATURE:
                print("Controller:", ATMEGA328PU_NAME_STRING)
            elif signature == ATMEGA328PB_SIGNATURE:
                print("Controller:", ATMEGA328PB_NAME_STRING)
            else:
                print("Unknown Controller")


def main():
    parser = argparse.ArgumentParser(description='Build Firmware for TQFP32 AVR Controller')

    parser.add_argument(
        "Mode",
        choices=[FIRMWARE_BUILD, FIRMWARE_FLASH, CONTROLLER_DETECT],
        help=f"Use '{FIRMWARE_BUILD}' or '{FIRMWARE_FLASH}' or '{CONTROLLER_DETECT}' for select the Mode"
    )

    args = parser.parse_args()
    print(f"Selected '{args.Mode}' Mode")
    builder = Builder(args.Mode)


if __name__ == "__main__":
    main()