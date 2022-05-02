def hex_to_int(hex):
    if hex == "0":
        return 0
    elif hex == "1":
        return 1
    elif hex == "2":
        return 2
    elif hex == "3":
        return 3
    elif hex == "4":
        return 4
    elif hex == "5":
        return 5
    elif hex == "6":
        return 6
    elif hex == "7":
        return 7
    elif hex == "8":
        return 8
    elif hex == "9":
        return 9
    elif hex == "A":
        return 10
    elif hex == "B":
        return 11
    elif hex == "C":
        return 12
    elif hex == "D":
        return 13
    elif hex == "E":
        return 14
    elif hex == "F":
        return 15
    else:
        return "-"


def process_ip_address(ip_address):
    # cut into 4 parts
    ip_address_part_1 = ip_address[0:2]
    ip_address_part_2 = ip_address[2:4]
    ip_address_part_3 = ip_address[4:6]
    ip_address_part_4 = ip_address[6:8]
    # first part will tell u class
    class_indicator = (16 * hex_to_int(ip_address_part_1[0])) + hex_to_int(ip_address_part_1[1])
    # print(class_indicator)
    ip_class = ""
    network_id = ""
    host_id = ""
    dotted_decimal = ""
    if class_indicator < 128:
        # print("Class A")
        ip_class = "A"
        network_id = ip_address_part_1
        host_id = ip_address_part_2 + ip_address_part_3 + ip_address_part_4

    elif class_indicator <= 191:
        # print("Class B")
        ip_class = "B"
        network_id = ip_address_part_1 + ip_address_part_2
        host_id = ip_address_part_3 + ip_address_part_4
    else:
        # print("Class C")
        ip_class = "C"
        network_id = ip_address_part_1 + ip_address_part_2 + ip_address_part_3
        host_id = ip_address_part_4

    dotted_decimal = str(16 * hex_to_int(ip_address_part_1[0]) + hex_to_int(ip_address_part_1[1])) \
                     + "." + str(16 * hex_to_int(ip_address_part_2[0]) + hex_to_int(ip_address_part_2[1])) \
                     + "." + str(16 * hex_to_int(ip_address_part_3[0]) + hex_to_int(ip_address_part_3[1])) \
                     + "." + str(16 * hex_to_int(ip_address_part_4[0]) + hex_to_int(ip_address_part_4[1]))

    print("Class = " + ip_class)
    print("Network ID = " + network_id)
    print("Host ID = " + host_id)
    print("Dotted Decimal = " + dotted_decimal)
    print("\n")
    # print(ip_class + "\n" + network_id + "\n" + host_id + "\n" + dotted_decimal + "\n")
    # then 3 conditional statements each which prints the object of [class, networkID, hostID, dottedDecimal]


def process_text(path):
    questions = []
    with open(path) as f:
        for line in f:
            questions.append(line[:-1])

    for question in questions:
        print(question)
        process_ip_address(question)


process_text("HW 2.txt")
