import subprocess

def invoke_web_request(url, outfile):
    powershell_script = f'Invoke-WebRequest -Uri "{url}" -OutFile "{outfile}"'
    subprocess.run(['powershell', '-Command', powershell_script])

if __name__ == "__main__":
    url = "https://github.blog/2022-06-03-a-beginners-guide-to-ci-cd-and-automation-on-github/"
    outfile = r"C:\Users\Ron\Desktop\Ron's Wiki's\CICD.html"  # Adjust the path as needed
    invoke_web_request(url, outfile)
