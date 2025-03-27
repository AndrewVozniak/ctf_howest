# CTF Challenge: "Internal System"

## Challenge Description

**Category:** Web Pentesting  
**Difficulty:** Easy/Medium  

**Question:**  
We've discovered an internal company portal that might be leaking sensitive information. Can you find a way in and retrieve the flag?  

**URL:** http://127.0.0.1:5000

## Hints

1. Sometimes, developers leave sensitive files exposed. Try looking for hidden or backup files.
2. Default credentials are often overlooked by system administrators.
3. The robots.txt file can sometimes reveal interesting paths.

## Challenge Setup


### Requirements for deployment:
- Python
- Flask
- SQLite
- Web Server
- Docker ( for easy deployment )

### Requirements for user:
- Docker 

### Steps to Reproduce:
1. **Create a simple login portal:**  
   - Use Python & Flask to create a basic login page (`/`).
   - Store credentials in a database (`app.db`) and files in a directory (`static`).
   - Use weak username (`admin`) for the admin account.
 
2. **Add a hidden admin panel:**  
   - Create a basic admin panel (`/admin`) and create html  for the same.
   - The admin panel allows access to the internal files including flag hidden in the zip file (`secret_key.zip/secret_key.txt`).
3. **Place a hidden logs and credentials files:**  
   - Add an exposed `logs` file containing `config.php` with the database credentials.
   
4. **Add `logs.txt` and `credentials.txt`:**  
   - The `logs.txt` file should contain a hint to check the `credentials.txt` file.
   - The `credentials.txt` file contains about 350 passwords and usernames, including the valid admin credentials. All of them should be in base64 format.
   
5. **Add `robots.txt`:**  
   - Include an entry pointing to `/logs.txt` and `/credentials.txt`.
   
6. **Deploy using Docker (optional):**  
   ```dockerfile
   FROM python:3.10
   WORKDIR /app
   COPY . /app
   RUN pip install --no-cache-dir -r requirements.txt
   EXPOSE 5000
   CMD ["python", "app.py"]
   ```
   - Run `docker build -t ctf_howest .` and `docker run -p 5000:5000 ctf_howest`.

## Solution
1. **Download docker image and run it:**  
   - Run `docker pull dzonkan/ctf:latest` and `docker run -p 5000:5000 dzonkan/ctf:latest`

2. **Check for publicly available files:**  
   - Access `robots.txt` to find `/admin/`.
   - Visit `/admin` to find an unprotected panel.

3. **Try default credentials:**  
   - Try to bruteforce admin credentials. If no then look for `credentials.txt` and decode the base64 strings.
   - Use the decoded credentials to brute force the admin login.
   
4. **Look for internal files:**  
   - Locate `secret_key.zip` and download it.
   
5. **Retrieve the flag:**  
   - Extract a flag from `secret_key.txt`
   
**Flag Format:** `CTF{Web_Pentest_Success_XXXXXXXX}`

## Recreating the Challenge
To deploy this challenge, simply follow the setup steps above, ensuring that the server is accessible to CTF participants. Using Docker simplifies the process, making it easily replicable on any system.
But if you prefer to download source code and run it manually, then you can use this repository: https://github.com/AndrewVozniak/ctf_howest.git