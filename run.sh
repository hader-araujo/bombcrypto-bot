#/bin/bash
if [[ "$OSTYPE" == "darwin"* ]]; then
  pip install -r requirements-mac.txt
else
  pip install -r requirements.txt
fi

python index.py