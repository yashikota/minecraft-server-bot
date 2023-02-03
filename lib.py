import re

def get_logged_in_user(log):
    regex = r"\[\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\]"
    with open(log, "r") as f:
        return [re.sub(regex, "", (line.split(" ")[4])) for line in f if "logged in with entity" in line]

def get_logged_out_user(log):
    regex = r"\[\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\]"
    with open(log, "r") as f:
        return [re.sub(regex, "", (line.split(" ")[4])) for line in f if "lost connection" in line]

def main():
    file_path = "../mc/nohup.out"
    logged_in_user = get_logged_in_user(file_path)
    print(logged_in_user)

if __name__ == "__main__":
    main()

