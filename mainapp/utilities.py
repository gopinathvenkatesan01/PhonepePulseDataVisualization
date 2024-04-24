def formated(number):
    number_str = str(number)
    length = len(number_str)
    formatted_number = ""
    comma_counter = 0
    for i in range(length - 1, -1, -1):
        formatted_number = number_str[i] + formatted_number
        comma_counter += 1
        if comma_counter == 2 and i != 0:
            formatted_number = "," + formatted_number
            comma_counter = 0
        elif comma_counter == 3 and i != 0:
            formatted_number = "," + formatted_number
            comma_counter = 0
    return formatted_number


def amount_crores(number):
    return '₹'+'{:,.0f} Cr'.format(round(number / 10000000))

def amount_rupees(number):
    return'₹'+'{:,.0f}'.format(round(number))

def formated(number):
    number_str = str(number)
    length = len(number_str)
    formatted_number = ""
    comma_counter = 0
    for i in range(length - 1, -1, -1):
        formatted_number = number_str[i] + formatted_number
        comma_counter += 1
        if comma_counter == 2 and i != 0:
            formatted_number = "," + formatted_number
            comma_counter = 0
        elif comma_counter == 3 and i != 0:
            formatted_number = "," + formatted_number
            comma_counter = 0
    return formatted_number