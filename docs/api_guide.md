# URL API Documentation

This API provides endpoints for managing URLs.

## Create URL

Create a new URL.

**URL:** `/urls/url/`
**Method:** `POST`

### Request Body

- `url_data` (dict, required): Data to create the URL.

### Response

Returns a dictionary with the created URL information.

### Errors

- 500 Internal Server Error: If an error occurs during creation.

## Read URL

Get information about a URL by its ID.

**URL:** `/urls/url/{url_id}`
**Method:** `GET`

### Path Parameters

- `url_id` (int, required): ID of the URL to retrieve.

### Response

Returns a dictionary with the URL information.

### Errors

- 404 Not Found: If the URL is not found.
- 500 Internal Server Error: If an error occurs during retrieval.

## Update URL

Update information about a URL.

**URL:** `/urls/url/{url_id}`
**Method:** `PUT`

### Path Parameters

- `url_id` (int, required): ID of the URL to update.

### Request Body

- `url_data` (dict, required): New data for the URL.

### Response

Returns a dictionary with a status message indicating successful update.

### Errors

- 404 Not Found: If the URL is not found.
- 500 Internal Server Error: If an error occurs during update.

## Delete URL

Delete a URL by its ID.

**URL:** `/urls/url/{url_id}`
**Method:** `DELETE`

### Path Parameters

- `url_id` (int, required): ID of the URL to delete.

### Response

Returns a dictionary with a status message indicating success or failure.

### Errors

- 404 Not Found: If the URL is not found.
- 500 Internal Server Error: If an error occurs during deletion.


