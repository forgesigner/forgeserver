import requests
from config import API_KEY


# EXAMPLE USAGE

def download_file(url, local_filename, headers):
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


if __name__ == '__main__':
    # UPLOAD FILES

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

    # DOWNLOAD CHECKPOINT

    url = 'http://34.16.177.159:5000/download_checkpoint'
    local_filename = 'test.onnx'

    downloaded_file = download_file(url, local_filename, headers=headers)
    print(f"File downloaded as: {downloaded_file}")
