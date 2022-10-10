from hashlib import sha256
import time
import multiprocessing


def brute_force(hashes, first_ind_letter, last_ind_letter, queue):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    possible_passwords = []

    for letter1 in letters[first_ind_letter: last_ind_letter if last_ind_letter < len(letters) else len(letters)]:
        for letter2 in letters:
            for letter3 in letters:
                for letter4 in letters:
                    for letter5 in letters:
                        possible_passwords.append(letter1+letter2+letter3+letter4+letter5)
    with open('newfile.txt', 'w', encoding='utf-8') as g:
        for word in possible_passwords:
            g.write(word)
    found_passwords = []
    for password in possible_passwords:
        hash = sha256(password.encode("UTF-8"))
        if hash.hexdigest() in hashes:
            found_passwords.append(password)
    queue.put(found_passwords)
    return found_passwords

def generate_indexes(num_process):
    step = int(26/num_process+1)
    indexes_list = []
    i = 0
    while i < 26:
        indexes_list.append(i)
        i += step

    return indexes_list, step


if __name__ == '__main__':
    hashes = ['1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad',
              '3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b',
              '74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f']
    num_of_process = int(input("Введите количетсво процессов: "))
    ind_list, step = generate_indexes(num_of_process)
    process_list = []
    queue = multiprocessing.Queue()
    for i in range(num_of_process):
        process = multiprocessing.Process(target=brute_force, args=(hashes, ind_list[i], step+ind_list[i], queue))
        process_list.append(process)
    start_time = time.time()
    for p in process_list:
        p.start()

    for p in process_list:
        p.join()
    print(time.time() - start_time)
    found_passwords = []
    while queue.qsize() > 0:
        pass_list = queue.get()
        for password in pass_list:
            found_passwords.append(password)

    print(found_passwords)