import pyzipper
import itertools

digits = '012'

for c in itertools.product(digits, repeat=15):
  password = ''.join(c)
  try:
    with pyzipper.AESZipFile('E6C63.zip', 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as extracted_zip:
      extracted_zip.extractall(pwd=str.encode(password))
      break
  except:
    # print(password)
    pass
    
pwd = bytes(password, 'utf-8')
print(pwd)