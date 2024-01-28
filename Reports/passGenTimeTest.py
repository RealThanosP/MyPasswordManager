import time
from PassGen import PassGenerator
from itertools import product
# Purpose of this script: To test the .generate_password() method of PassGenerator class.

# This method is basiclly a big while loop that stops when the desired length of the password is met.
# So there where some instances especially with only the easy_to_remeber srt to True, where the method got stuck cause it could not find a word 
# thats like under 2-3 chars long. I tried to fix it by adding the lowercase and the real_words in the allowed chars when easy_to_remember = True. 

# Summary: Its preetty fast with the combined real_word+lowercase list the while loop doen't stuck and crashes anymore.

# The passwords might be a little not memorable but the 3000 words that are being used are way to many to be overwhelmed by the letters
# It seems like the most important factor is not the length but rather the different combinations of settings.

# Avrg time in 5000 iterations based on length can be found in the spreadsheet
# I chose 5000 iterations because it's not supposed to be run a lot of times again and again by the user
# Increasing the order of magnitude of the test to 5*10^4 is kind of unrealistic and too much

def test():
    boolean_combinations = list(product([True, False], repeat=4))
    for length in range(10, 51):
        avrg_time = 0
        times = []
        for j in range(16):
            #Skips the all false case
            if boolean_combinations[j] == (False, False, False, False): 
                continue
            #Test loop for 10_000 times
            for i in range(5_000):
                gen = PassGenerator(length, *boolean_combinations[j])
                t_start = time.process_time()
                random_password = gen.generate_password() 
                t_end_ms = 1000*(time.process_time() - t_start)
                times.append(t_end_ms)
                avrg_time = sum(times)/len(times)
            
            spreadsheet_line = f"{avrg_time:.5f}\t{length}\t{boolean_combinations[j][0]}\t{boolean_combinations[j][1]}\t{boolean_combinations[j][2]}\t{boolean_combinations[j][3]}"
            print(spreadsheet_line)
            with open("test_times.txt", "a", encoding="utf-8") as file:
                file.write(f"{spreadsheet_line}\n")
            
if __name__ == '__main__':
    test()

