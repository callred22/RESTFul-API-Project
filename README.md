# What this does

## CHECK TO SEE IF database is filled, if not then it pre-fills data from apis into local database


## GET
User sends blank get request to api and receives average totals per state (medicare/zipcodes & covid/zipcodes) as JSON


## POST (user-specific)
User sends PUT request to API with the following parameters:
 - user (pincode for a user(unique))
 - state
 - zip

The user gets saved into the database with the state and zipcode, after which they can pull the information with a GET request to get their specific information as shown below:

## GET (user-specific)
User sends GET request to api with the following parameters:
 - user (pincode for user (already created in POST request))

The user will receive information partaining to their originally created state and zipcode

## PATCH (user-specific)
User sends PATCH request to api with the following parameters:
 - user (required(pincode for user (already created in POST request)))
 - state (optional)
 - zip (optional)

Even though these are optional, one will have to be used or it will send back a 500 response (missing information)
