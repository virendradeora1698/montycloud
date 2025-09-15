# File Upload APIs – Django App

This Django app provides a set of APIs for uploading, listing, updating, and deleting images. It also stores image metadata (like name, user, and URL).  

The base URL is:
```
http://127.0.0.1:8000/app/
```

---

## 1. List all images
- **Method:** GET  
- **Endpoint:** `/images`  
- **Example:**  
  ```
  http://127.0.0.1:8000/app/images
  ```

### Response
```json
[
  {
    "id": "7",
    "name": "AAY_1_AAY_2.jpeg",
    "user": "umi",
    "image_url": "http://localhost:4566/my-first-bucket/uploads/AAY_1_AAY_2.jpeg"
  }
]
```

---

## 2. Upload a new image
- **Method:** POST  
- **Endpoint:** `/upload/`  
- **Example:**  
  ```
  http://127.0.0.1:8000/app/upload/
  ```

### Request (form-data)
- `image` → the image file  
- `user` → the username  

### Curl Example
```bash
curl -X POST http://127.0.0.1:8000/app/upload/   -F "image=@C:/Users/ummed/Downloads/sample.jpeg"   -F "user=umi"
```

### Response
```json
{
  "id": "7",
  "name": "sample.jpeg",
  "user": "umi",
  "image_url": "http://localhost:4566/my-first-bucket/uploads/sample.jpeg"
}
```

---

## 3. Get an image by ID
- **Method:** GET  
- **Endpoint:** `/image/{id}/`  
- **Example:**  
  ```
  http://127.0.0.1:8000/app/image/7/
  ```

### Response
```json
{
  "id": "7",
  "name": "sample.jpeg",
  "user": "umi",
  "image_url": "http://localhost:4566/my-first-bucket/uploads/sample.jpeg"
}
```

If the image doesn’t exist:
```json
{
  "error": "Image not found."
}
```

---

## 4. Delete an image by ID
- **Method:** DELETE  
- **Endpoint:** `/image/{id}/delete/`  
- **Example:**  
  ```
  http://127.0.0.1:8000/app/image/7/delete/
  ```

### Response
```json
{
  "message": "Image with id=7 deleted successfully."
}
```

---

## 5. Update an image by ID
- **Method:** PUT  
- **Endpoint:** `/image/{id}/update/`  
- **Example:**  
  ```
  http://127.0.0.1:8000/app/image/7/update/
  ```

### Headers
```
Content-Type: application/json
```

### Request Body
```json
{
  "name": "new_name.jpg",
  "user": "umi"
}
```

### Response
```json
{
  "id": "7",
  "name": "new_name.jpg",
  "user": "umi",
  "image_url": "http://localhost:4566/my-first-bucket/uploads/new_name.jpg"
}
```

---

## How to Use
1. Start your Django server:
   ```bash
   python manage.py runserver
   ```
2. If you’re using LocalStack for S3 storage, make sure it’s running:
   ```bash
   localstack start -d
   ```
3. Test the APIs using:
   - Browser (for GET requests)  
   - Postman / Thunder Client  
   - Curl (examples above)  

**Typical workflow:**  
- Upload → `POST /upload/`  
- Fetch details → `GET /image/{id}/`  
- Update metadata → `PUT /image/{id}/update/`  
- Delete → `DELETE /image/{id}/delete/`  

---
