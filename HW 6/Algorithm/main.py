import numpy as nm
import pynput

import pytesseract

import cv2

import pyscreenshot

import bbox

from PIL import Image

"D3990RA5EB838632DC4C2352080045DE" \
"007246C24A005B3E09C28C7BB424DE0C" \
"DBF7644DB5BF6E10CBA7BEB807C99CD8"


def bin_to_hex(bin):
    if bin == "0":
        return "0"
    elif bin == "1":
        return "1"
    elif bin == "0000":
        return "0"
    elif bin == "0001":
        return "1"
    elif bin == "0010":
        return "2"
    elif bin == "0011":
        return "3"
    elif bin == "0100":
        return "4"
    elif bin == "0101":
        return "5"
    elif bin == "0110":
        return "6"
    elif bin == "0111":
        return "7"
    elif bin == "1000":
        return "8"
    elif bin == "1001":
        return "9"
    elif bin == "1010":
        return "A"
    elif bin == "1011":
        return "B"
    elif bin == "1100":
        return "C"
    elif bin == "1101":
        return "D"
    elif bin == "1110":
        return "E"
    elif bin == "1111":
        return "F"
    else:
        return "-"


def hex_to_bin(hex):
    if hex == "0":
        return "0000"
    elif hex == "1":
        return "0001"
    elif hex == "2":
        return "0010"
    elif hex == "3":
        return "0011"
    elif hex == "4":
        return "0100"
    elif hex == "5":
        return "0101"
    elif hex == "6":
        return "0110"
    elif hex == "7":
        return "0111"
    elif hex == "8":
        return "1000"
    elif hex == "9":
        return "1001"
    elif hex == "A":
        return "1010"
    elif hex == "B":
        return "1011"
    elif hex == "C":
        return "1100"
    elif hex == "D":
        return "1101"
    elif hex == "E":
        return "1110"
    elif hex == "F":
        return "1111"
    else:
        return "-"


def flags_and_fragment(data):
    binary = hex_to_bin(data[0]) + hex_to_bin(data[1]) + hex_to_bin(data[2]) + hex_to_bin(data[3])
    # print(binary)
    first_three_bits = binary[0:3]
    reserved = first_three_bits[0]
    fragment = "Don't Fragment" if first_three_bits[1] == '1' else "Fragment"
    more_fragments = "More Fragments" if first_three_bits[2] == '1' else "No More Fragments"
    fragment_offset_bin_4 = binary[12:16]
    # print(fragment_offset_bin_4)
    fragment_offset_bin_3 = binary[8:12]
    # print(fragment_offset_bin_3)
    fragment_offset_bin_2 = binary[4:8]
    # print(fragment_offset_bin_2)
    fragment_offset_bin_1 = binary[3:4]
    # print(fragment_offset_bin_1)

    # print(hex(int(fragment_offset_bin_4, 2)))
    # print(hex(int(fragment_offset_bin_3, 2)))
    # print(hex(int(fragment_offset_bin_2, 2)))
    # print(hex(int(fragment_offset_bin_1, 2)))

    fragment_offset = bin_to_hex(fragment_offset_bin_1) + bin_to_hex(fragment_offset_bin_2) + bin_to_hex(
        fragment_offset_bin_3) + bin_to_hex(fragment_offset_bin_4)

    # print(fragment_offset)

    return [
        data,
        fragment,
        more_fragments + " " + first_three_bits,
        fragment_offset
    ]

    # 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
    # 0 1 2 3 4 5 6 7 8 9 101112131415


def ip_address(data):
    print(data)
    first_part = data[0]
    first_part_decimal = int(first_part, 16)
    ip_address_class = ""
    ip_address_network = ""
    ip_address_host = ""
    if first_part_decimal <= 126:
        ip_address_class = "A"
        ip_address_network = data[0]
        ip_address_host = data[1] + data[2] + data[3]
    elif 128 <= first_part_decimal <= 191:
        ip_address_class = "B"
        ip_address_network = data[0] + data[1]
        ip_address_host = data[2] + data[3]
    elif 192 <= first_part_decimal <= 223:
        ip_address_class = "C"
        ip_address_network = data[0] + data[1] + data[2]
        ip_address_host = data[3]

    dotted_decimal = str(int(data[0], 16)) + "." + str(int(data[1], 16)) + "." + str(int(data[2], 16)) + "." + str(
        int(data[3], 16))

    return [
        data[0] + data[1] + data[2] + data[3],
        ip_address_class,
        ip_address_network,
        ip_address_host,
        dotted_decimal
    ]


def process_datagram(path):
    datagram = []
    data_line = []

    with open(path) as f:
        for line in f:
            data_line = line.split(" ")
            datagram.append(data_line)

    destination_hardware_address = ""
    for i in range(0, 6):
        destination_hardware_address += datagram[0][i]
    print("Destination Hardware Address = ", destination_hardware_address)

    source_hardware_address = ""
    for i in range(6, 12):
        source_hardware_address += datagram[0][i]
    print("Source Hardware Address = ", source_hardware_address)

    frame_type = ""
    for i in range(12, 14):
        frame_type += datagram[0][i]
    print("Frame Type = ", frame_type + "\n")

    vers_and_lens = datagram[0][14]
    print("Vers & Lens = ", vers_and_lens)

    type_of_service = datagram[0][15][:-1]
    print("Type Of Service = ", type_of_service)

    total_length = ""
    for i in range(0, 2):
        total_length += datagram[1][i]
    print("Total Length = ", total_length)

    ident = ""
    for i in range(2, 4):
        ident += datagram[1][i]
    print("Ident = ", ident + "\n")

    # FLAGS AND FRAGMENT
    fragment_data = flags_and_fragment(datagram[1][4] + datagram[1][5])
    # fragment_data = flags_and_fragment("7BC7")
    flags_and_fragment_offset = fragment_data[0]
    flags = fragment_data[1] + " " + fragment_data[2]
    fragment_offset = fragment_data[3][:2] + fragment_data[3][2:]
    print("Flags & Fragment Offset = ", flags_and_fragment_offset)
    print("Flags = ", flags)
    print("Fragment Offet = ", fragment_offset + "\n")

    ttl = datagram[1][6]
    print("TTL = ", ttl)

    type = datagram[1][7]
    print("Type = ", type)

    header_checksum = ""
    for i in range(8, 10):
        header_checksum += datagram[1][i]
    print("Header Checksum = ", header_checksum + "\n")

    # SOURCE IP ADDRESS

    source_ip_address_data = ip_address([datagram[1][10], datagram[1][11], datagram[1][12], datagram[1][13]])
    source_ip_address = source_ip_address_data[0]
    print("Source IP Address = ", source_ip_address)
    source_ip_address_class = source_ip_address_data[1]
    print("Class = ", source_ip_address_class)
    source_ip_address_network = source_ip_address_data[2]
    print("Network = ", source_ip_address_network)
    source_ip_address_host = source_ip_address_data[3]
    print("Host = ", source_ip_address_host)
    source_ip_address_dotted_decimal = source_ip_address_data[4]
    print("Source IP Address (Decimal) = ", source_ip_address_dotted_decimal + "\n")

    # DESTINATION IP ADDRESS
    destination_ip_address_data = ip_address([datagram[1][14], datagram[1][15][:-1], datagram[2][0], datagram[2][1]])
    destination_ip_address = destination_ip_address_data[0]
    print("Destination IP Address = ", destination_ip_address)
    destination_ip_address_class = destination_ip_address_data[1]
    print("Class = ", destination_ip_address_class)
    destination_ip_address_network = destination_ip_address_data[2]
    print("Network = ", destination_ip_address_network)
    destination_ip_address_host = destination_ip_address_data[3]
    print("Host = ", destination_ip_address_host)
    destination_ip_address_dotted_decimal = destination_ip_address_data[4]
    print("Destination IP Address (Decimal) = ", destination_ip_address_dotted_decimal + "\n")

    # UDP info
    source_port = ""
    for i in range(2, 4):
        source_port += datagram[2][i]
    print("Source Port = ", source_port)

    destination_port = ""
    for i in range(4, 6):
        destination_port += datagram[2][i]
    print("Destination Port = ", destination_port)

    udp_message_length = ""
    for i in range(6, 8):
        udp_message_length += datagram[2][i]
    print("UDP Message Length = ", udp_message_length)

    udp_checksum = ""
    for i in range(8, 10):
        udp_checksum += datagram[2][i]
    print("UDP Checksum = ", udp_checksum)

    payload_data = ""
    for i in range(10, 15):
        payload_data += datagram[2][i]
    print("Payload Data = ", payload_data)


# https://stackoverflow.com/questions/33949831/how-to-remove-all-lines-and-borders-in-an-image-while-keeping-text-programmatica
def remove_lines(file_name, result_file):
    image = cv2.imread(file_name)
    result = image.copy()
    # upscale = cv2.resize(result, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    clrs = Image.open("s22 midterm.PNG")
    pix = clrs.load()
    if pix[0, 0][3] == 0:
        thresh = 255 - thresh
    # print(type(pix[0,0][3]))
    invert = 255 - thresh

    # Remove horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(result, [c], -1, (255, 255, 255), 5)

    # Remove vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(result, [c], -1, (255, 255, 255), 5)

    cv2.imshow('thresh', thresh)
    cv2.imshow('invert', invert)
    cv2.imshow('result', result)
    cv2.imwrite(result_file, result)
    cv2.waitKey()


def algorithm(path):
    # https://nanonets.com/blog/ocr-with-tesseract/
    # https://stackoverflow.com/questions/58948775/is-it-possible-to-extract-text-from-specific-portion-of-image-using-pytesseract
    # https://stackoverflow.com/questions/9480013/image-processing-to-improve-tesseract-ocr-accuracy

    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\/tesseract.exe'

    image = cv2.imread(
        path,
        0)

    print(image.shape)
    thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    ROI = thresh[0:299, 0:1168]
    # https://stackoverflow.com/questions/46574142/pytesseract-using-tesseract-4-0-numbers-only-not-working

    # C:\Program Files\Tesseract-OCR\tessdata\configs <- for 'digits' config
    data = pytesseract.image_to_string(ROI, lang='eng', config='--psm 6 digits')

    print(data)

# remove_lines('s21 hw6.png', 's21 hw6 result.png')
# algorithm('s22 result.png')
# process_datagram('s22 hw6 datagram.txt')

# remove_lines('s22 midterm.PNG', 's22 midterm result.png')
# algorithm('midterm result.png')
# process_datagram('midterm.txt')
