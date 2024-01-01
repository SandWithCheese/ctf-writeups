import zipfile
import itertools

digits = '012'

for c in itertools.product(digits, repeat=15):
  password = ''.join(c)
  try:
    with zipfile.ZipFile('./large.zip', 'r') as zip_ref:
      print(password)
      zip_ref.extractall(path='./', pwd = bytes(password, 'utf-8'))
      break
  except:
    print('Password ' + password + ' failed')
    
pwd = bytes(password, 'utf-8')