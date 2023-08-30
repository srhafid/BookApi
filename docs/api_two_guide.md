# User API Documentation

This API provides endpoints for managing users.

## Create User

Create a new user.

**URL:** `/users/user/`
**Method:** `POST`

### Request Body

- `user_data` (dict, required): Data to create the user.

### Response

Returns a dictionary with the created user information.

### Errors

- 500 Internal Server Error: If an error occurs during creation.

## Read User

Get information about a user by its ID.

**URL:** `/users/user/{user_id}`
**Method:** `GET`

### Path Parameters

- `user_id` (int, required): ID of the user to retrieve.

### Response

Returns a dictionary with the user information.

### Errors

- 404 Not Found: If the user is not found.
- 500 Internal Server Error: If an error occurs during retrieval.

## Update User

Update information about a user.

**URL:** `/users/user/{user_id}`
**Method:** `PUT`

### Path Parameters

- `user_id` (int, required): ID of the user to update.

### Request Body

- `new_data` (dict, required): New data for the user.

### Response

Returns a boolean indicating if the user was updated successfully.

### Errors

- 404 Not Found: If the user is not found.
- 500 Internal Server Error: If an error occurs during update.

## Delete User

Delete a user by its ID.

**URL:** `/users/user/{user_id}`
**Method:** `DELETE`

### Path Parameters

- `user_id` (int, required): ID of the user to delete.

### Response

Returns a boolean indicating if the user was deleted successfully.

### Errors

- 404 Not Found: If the user is not found.
- 500 Internal Server Error: If an error occurs during deletion.
