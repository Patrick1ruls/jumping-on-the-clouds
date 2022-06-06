# Test Cases

## O = pass | X = fail

## GET /stats
* O User is able to pull "TotalRequests" and "AverageTime"
    * O "TotalRequests" matches the number of hash requests sent to the POST /hash endpoint
    * O "AverageTime" gives the average time for all POST /hash requests to process
* O Responds with 200 status code
* O Responds in under 100 ms

## POST /hash password
* O Sending a message in the proper format, {"password": "{message}"}, results in a hash being generated and id returned
* O Sending a message in the proper format results in a 200 status code
* O Sending 2 proper different messages results in 2 different hashs being generated
* O Takes 5 seconds for server to generate a hash
* O All requests sent in parallel are processed in the order that they're received
* O Sending an improper message, {"password": 0}, results in a 400 status code and "Malformed Input" response
* O Hash generation is not interupted by POST shutdown
* X Data contract should be enforced
* X Sending duplicate proper messages does NOT result in duplicate hashes being generated
    * X Duplicate messages are blocked
* X User is not able to generate hash collisions
* O System is able to handle multiple users generating hashes

## GET /hash
* O User is able to get hash with 200 status code by providing existing id
* O If user provides non existent id, system responds with 400 status code and "Hash not found" message
* O If user provides improper id, Ex. "v", "Random_text", "", system responds with 400 error and 'strconv.Atoi: parsing "{id}": invalid syntax' message
* O System is able to handle multiple users getting hashes

## POST /hash shutdown
* O User is able to gracefully shutdown hash server with 200 response by sending the message "shutdown" to /hash endpoint
* O All in progress hash generations are allowed to finish during shutdown
* O New hash requests are rejected during shutdown

