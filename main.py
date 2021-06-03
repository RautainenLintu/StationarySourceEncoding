import json
import fractions
import math


# Function asks for file name to find the file
def ask_for_file():
    while True:
        print("Enter filename for the source description:")
        filename = input()
        if len(filename) <= 0:
            print("The file name is empty. Try again")
        try:
            file = open(filename)
            file.close()
        except FileNotFoundError:
            print("The file is not found. Please check the existence and location of the file, then try again")
        else:
            break
    return filename


# Function checks if the source description is correct
def description_correct(description):
    correctness = True
    prob_sum = 0
    for probability in description.values():
        prob_sum += float(fractions.Fraction(probability))
    if prob_sum != 1:
        correctness = False
    return correctness


# Function counts entropy
def find_entropy(probabilities):
    entropy = 0
    for i in probabilities:
        if i != 0:
            entropy -= i * math.log2(i)
    return entropy


# Function generates high probability set
def generate_hps(source_dict, entropy, epsilon, n):
    high_probability_set = []
    for i in range(2 ** n):
        weight = bin(i).count('1')
        p = source_dict["1"] ** weight * source_dict["0"] ** (n - weight)
        if entropy - epsilon <= -math.log2(p) / n <= entropy + epsilon:
            high_probability_set.append(i)
    return high_probability_set


# Function generates coding words
def generate_coding_words(q, size):
    words = []
    m = 1
    while q ** m < size:
        m += 1
    for i in range(size):
        word = ""
        element = i
        for j in range(m):
            word += str(element % q)
            element //= q
        words.append(word)
    return words


# Function generates encoding
def generate_encoding(source_dict, entropy, R, epsilon, q):
    n = 1
    while True:
        hps_n = generate_hps(source_dict, entropy, epsilon, n)
        sum_p = 0
        for element in hps_n:
            p = 1
            for bit in bin(element)[2:]:
                p *= source_dict[bit]
            sum_p += p
        if sum_p >= 1 - (R - entropy):
            break
        n += 1
    code = generate_coding_words(q, len(hps_n))
    return code, hps_n


while True:
    filename = "source_description.json"
    # filename = ask_for_file()
    source_file = open(filename, "r")
    source_dict = json.load(source_file)
    if not description_correct(source_dict):
        print("Incorrect description. Try again")
        break
    for outcome in source_dict:
        source_dict[outcome] = float(fractions.Fraction(source_dict[outcome]))
    entropy = find_entropy(source_dict.values())
    encoded_file = open("encoded_file.txt", "w")
    print("Choose mode 1 (entropy calculating) or 2 (code generating):")
    mode = input()
    while mode != '1' and mode != '2':
        print("Incorrect mode. Try again:")
        mode = input()
    if mode == '1':
        print("Entropy: ", entropy)
    if mode == '2':
        while True:
            try:
                print("Enter R: ")
                R = float(input())
                print("Enter epsilon: ")
                epsilon = float(input())
                print("Enter q: ")
                q = int(input())
                if R < entropy:
                    print("The code cannot be generated. Entropy must not be greater than R")
                    print("Entropy: ", entropy)
                else:
                    code, hps_n = generate_encoding(source_dict, entropy, R, epsilon, q)
                    str = "Encoding: \n"
                    str += "{:<10}\t{}".format("HPS element", "Encoding word:\n")
                    for i in range(len(hps_n)):
                        str += "{:<10}\t{:<10}\n".format(hps_n[i], code[i])
                    encoded_file.write(str)
                    print("You can find your encoding in encoded_file.txt.")
                    break
            except ValueError as value_error:
                print("Incorrect value entered. Try again.")
    source_file.close()
    encoded_file.close()
    print()
    print("Program finished")
    print("Press Enter to restart")
    input()
