# RESTFul API Project 
## Submission by Criosanna Allred 
## U762 Spring 2024 University of South Carolina Upstate 

## Video presentation can be accessed via the file above or directly through this link to [YouTube][1]
[1]: https://youtu.be/9oioFLb4lWc "YouTube"

# What this API does: 

## CHECK TO SEE IF database is filled, if not then it pre-fills data from apis into local database

## GET
User sends blank get request to api and receives average totals per state (medicare/zipcodes & covid/zipcodes) as JSON
User can get user data (nothing private)
User can get all medicare data
User can get all Covid data

 - URLs
 - - /v1/medicare
 - - /v1/covid
 - - /v1/user/all


## PUT (user-specific)
User sends PUT request to API with the following parameters:
 - user (pincode for a user(unique))
 - state
 - zip

The user gets saved into the database with the state and zipcode, after which they can pull the information with a GET request to get their specific information as shown below:

 - URLs
 - - /v1/user?user=*userpincode*&state=*updatedstate*&zip=*updatedzip*
 Just change the state and zip arguments to whatever needs to be saved, you do have to include both state and zip.

## GET (user-specific)
User sends GET request to api with the following parameters:
 - user (pincode for user (already created in POST request))

The user will receive information partaining to their originally created state and zipcode

 - URLs
 - - /v1/user?user=*userpincode*

## PATCH (user-specific)
User sends PATCH request to api with the following parameters:
 - user (required(pincode for user (already created in POST request)))
 - state (optional)
 - zip (optional)

Even though these are optional, one will have to be used or it will send back a 400 response (bad request / missing information)

 - URLs
 - - /v1/user?user=*userpincode*&state=*updatedstate*&zip=*updatedzip*

## DELETE (user-specific)
You can also delete a user using the following parameters: 
 - user (pincode for a user(unique))

 - URLs
 - - /v1/user?user=*userpincode*