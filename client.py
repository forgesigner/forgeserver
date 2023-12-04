import requests
from config import API_KEY

# EXAMPLE USAGE

if __name__ == '__main__':

    url = 'http://34.16.177.159:5000/upload'
    headers = {'Authorization': API_KEY}
    file_pairs = [
        ('/home/xram/Desktop/1.json', '/home/xram/Desktop/1.png'),
        ('/home/xram/Desktop/2.json', '/home/xram/Desktop/2.png'),
    ]

    files = {}
    for i, (file1_path, file2_path) in enumerate(file_pairs):
        files[f'annot_{i}'] = open(file1_path, 'rb')
        files[f'image_{i}'] = open(file2_path, 'rb')

    response = requests.post(url, headers=headers, files=files)
    for file in files.values():
        file.close()
