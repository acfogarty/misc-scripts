import re
import collections
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

"""
crypto par alphabet desordonné
"""

cleartext = "MESSAGE A CHIFFRER"
secretkey = "BAGUETTEMAGIQUE"

# tout supprimer a part les lettres et les espaces
cleartext = re.sub(r'[^\w\s\.]','',cleartext)

# convertir en majuscules si necessaire
cleartext = cleartext.upper()
secretkey = secretkey.upper()

# lettres majuscules de l'alphabet a partir des codes ascii
alphabet = [chr(l) for l in range(65, 91)]

# mot -> lettres
secretkey = list(secretkey)

# unique letters (ordered)
secretkey = list(collections.OrderedDict.fromkeys(secretkey))

# toutes les lettres qui ne sont pas dans la cle secrete
remaining_letters = [c for c in alphabet if c not in secretkey]

alphabet_encrypted = secretkey + remaining_letters

# ajouter des espaces
alphabet.extend([' ', '.'])
alphabet_encrypted.extend([' ', '.'])

# mapping entre lettres du message et lettres encryptees
mapping = dict(zip(alphabet, alphabet_encrypted))
reverse_mapping = dict(zip(alphabet_encrypted, alphabet))

print('dictionnaire originale -> encrypte:')
pprint(mapping)

print('dictionnaire encrypte -> originale:')
pprint(reverse_mapping)

# encrypter le message
codetext = ""
for c in cleartext:
  codetext += mapping[c]
print('message originale:')
print(cleartext)
print('message encrypte:')
print(codetext)

# histogramme (frequence des lettres)
letters = list(codetext)
counter=collections.Counter(letters)
plt.bar(range(len(counter)), counter.values(), width=1)
plt.xticks(range(len(counter)), counter.keys())
plt.show()
