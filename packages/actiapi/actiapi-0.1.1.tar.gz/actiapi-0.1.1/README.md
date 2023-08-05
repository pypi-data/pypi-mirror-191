ActiAPI
==============================
Encapsulate ActiGraph's API in an easy-to-use python package.

# Example

## Metadata
```python
from actiapi.v3 import ActiGraphClientV3

api_client = ActiGraphClientV3(<api_access_key>, <api_secret_key>)
metadata = api_client.get_study_metadata(<study_id>)
metadata = {x["id"]: x for x in metadata}
```

## Raw data
```python
from actiapi.v3 import ActiGraphClientV3

api_client = ActiGraphClientV3(<api_access_key>, <api_secret_key>)
results: List[str] = api_client.get_files(
            user=<user_id>, study_id=<self.study_id>
        )
```