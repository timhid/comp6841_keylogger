from cryptography.fernet import Fernet

key = "_Xsx521ZIOq3YSE6Ox0EnBkG6Mv8DfPQ-eff0ZArPAQ="

log_dir = "e_key_log.txt"
with open(log_dir, 'rb') as f:
    data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    
    with open("decryption.txt", 'ab') as f:
        f.write(decrypted)
