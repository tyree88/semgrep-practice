import json
import pickle
import yaml

data = b"..."

# ruleid: insecure-deserialization
pickle.loads(data)

# ruleid: insecure-deserialization
yaml.load(data, Loader=yaml.Loader)

# ruleid: insecure-deserialization
yaml.unsafe_load(data)

# ok: insecure-deserialization
yaml.load(data, Loader=yaml.SafeLoader)

# ok: insecure-deserialization
yaml.safe_load(data)

# ok: insecure-deserialization
json.loads(data)

# ruleid: insecure-deserialization
yaml.load_all(data, Loader=yaml.Loader)

# ruleid: insecure-deserialization
yaml.unsafe_load_all(data)

# ok: insecure-deserialization
yaml.load(data, yaml.SafeLoader)

# ok: insecure-deserialization
yaml.load(data, Loader=yaml.BaseLoader)
