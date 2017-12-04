import os

for parent, dirnames, filenames in os.walk('./'):
    for fn in filenames:
        if fn.lower().endswith('.pdf'):
            os.remove(os.path.join(parent, fn))