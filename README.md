# RESTFul API Project 
Submission by Criosanna Allred 

U762 Spring 2024 University of South Carolina Upstate 

The video presentation for this project can be accessed via the file above or directly through this link to YouTube: https://youtu.be/9oioFLb4lWc

# What this API does: 

## The first step is check to see if the database is filled. If not, then it pre-fills data from APIs into local database. 

## GET Request 
User sends blank get request to api and receives average totals per state (medicare/zipcodes & covid/zipcodes) as JSON
User can get user data (nothing private)
User can get all medicare data
User can get all Covid data

 - URLs
 - - /v1/medicare
 - - /v1/covid
 - - /v1/user/all


## PUT Request (user-specific)
User sends PUT request to API with the following parameters:
 - user (unqiue pincode for a user)
 - state (abbreviation only)
 - zip code (5-digit)

The user gets saved into the database with the state and zip code, after which they can pull the information with a GET request to get their specific information as shown below:

 - URLs
 - - /v1/user?user=*userpincode*&state=*updatedstate*&zip=*updatedzip*
 Just change the state and zip arguments to whatever needs to be saved, you do have to include both state and zip.

## GET Request (user-specific)
User sends GET request to api with the following parameters:
 - user (pincode user created in POST request)

The user will receive information partaining to their originally created state and zip code. 

 - URLs
 - - /v1/user?user=*userpincode*

## PATCH/UPDATE Request (user-specific)
User sends PATCH request to api with the following parameters:
 - user (user pincode required)
 - state (optional)
 - zip (optional)

Even though these are optional, one will have to be used or it will send back a 400 response (bad request/missing information). 

 - URLs
 - - /v1/user?user=*userpincode*&state=*updatedstate*&zip=*updatedzip*

## DELETE Request (user-specific)
You can also delete a user using the following parameters: 
 - user (unique pincode for the user)

 - URLs
 - - /v1/user?user=*userpincode*