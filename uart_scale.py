# Nima Mahdion

# https://pyserial.readthedocs.io/en/latest/shortintro.html

# This code is for using the UART serial port named /dev/ttyUSB
# to send and receive plaintexts and ciphertexts to the SCALE board.
# The cortex-m3 located on target board performs a masked AES which
# is written in assembly by Si Gao.

import serial
import os
from time import sleep


def uart(ser_port, num_repeat):
    """ This function enables the serial_port, and transmits tx_data
        from the PC to the device connected with the PC and receives
        rx_data from the device to the PC. Also it repeats the TX and RX
        transactions num_repeat times"""

    # The length of the input_data (TX data)
    # In the implementation of ASM_MaskedAES (written by Si Gao),
    # """ In the SCALE version, we ask for 6 bytes fresh random bytes
    # from the serial port, which eliminates the need for generating
    # randomness on board."""
    # MaskedAES.c ---> lines : 90-90
    # The first 16 bytes considered as plaintext, and the rest 4 bytes are:
    # 1 byte: Masking state
    # 1 byte: Masking round key
    # 4 bytes for different uses like Sbox, Mixcolumn and ...

    input_data_length = 16 + 6

    # The length the ciphertext (RX data)
    ciphertext_length = 16

    # Enabling the serial port
    serial_p = serial.Serial(ser_port)

    if serial_p.is_open:
        print("\n ********************* START ********************* \n")

    for i in range(num_repeat):

        # Generating a random plaintext
        input_data = os.urandom(input_data_length)

        # Wait
        # tx: Transmitting plaintext serially from the PC to the SCALE_Board by UART Serial Port
        sleep(0.01)
        serial_p.write(input_data)

        # rx: Receiving ciphertext serially from the SCALE_Board to the PC  by UART Serial Port
        ciphertext = serial_p.read(ciphertext_length)

        # Separating plaintext and random bytes
        plaintext = input_data[0:16]
        random_byte = input_data[16:22]

        # Printing plaintext and the corresponding ciphertext
        print('- Plaintext  {}:  [{}]'.format(i, plaintext.hex()))
        print('- Ciphertext {}:  [{}]'.format(i, ciphertext.hex()))
        print('\n - Random bytes {}:  [{}]'.format(i, random_byte.hex()))

        print('___________________________________________________________________')

    print('Serial port: {}'.format(serial_p.name))
    print('___________________________________________________________________')

    # Disabling the serial port
    serial_p.close()

    if not serial_p.is_open:
        print("\n ********************* END ********************* \n")

    return


if __name__ == '__main__':
    serial_port = '/dev/ttyUSB0'

    # The number of encryption
    num = 10
    uart(serial_port, num)
