# Bug Report

## 1 - Duplicate hashes
* Expected: When a user inputs the same password multiple times. Duplicate requests are either blocked or ignored
* Result: Each duplicate entry is accepted and generates a duplicate hash with a different id
* How to reproduce:
    * Send the request ```{"password": "lion heart}``` to ```POST /hash``` twice
    * 2 hash id's are generated, record these
    * Enter both hash id's into ```GET /hash```
    * Compare both hashes to see their the same

## 2 - Colliding hashes
* Expected: If a user enters any message format other than ```{"password": "<some_value>"}``` it should generate different hashes
* Result: The same hash is generated
* How to reproduce:
    * Send ```{"new_password": "something"}``` and ```{"other_password": "something_different"}``` to ```POST /hash```
    * 2 hash id's are generated, record these
    * Enter both hash id's into ```GET /hash```
    * Compare both hashes to see their the same

## 3 - No data contract enforced
* Expected: User should be rejected from sending any password that doesn't match the format ```{"password": "<some_value>"}```
* Result: Other formats are accepted which has resulted in the Collidign hashes bug described above
* How to reproduce: 
    * send the following message to ```POST /hash```
        ```
        {
            "data": {
                "more_data": {
                    "Nested": "json"
                }
            }
        }
        ```
    * Message is accepted with 200 response
