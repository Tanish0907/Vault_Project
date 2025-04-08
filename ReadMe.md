# Pixel Lock - Secure Image Gallery

---

## Overview
Pixel Lock is a secure image gallery application that allows users to upload, encrypt, and view images with privacy and security in mind. The application leverages blockchain technology and IPFS (InterPlanetary File System) to securely store and manage images. It provides a seamless user experience with a React-based frontend and a FastAPI backend.

---

## Features
1. **User Authentication**:
   - Users can register and log in using a unique authentication token.
   - Authentication tokens are securely generated and stored.

2. **Image Upload**:
   - Users can upload images with optional privacy settings.
   - Images are encrypted before being stored.

3. **Blockchain Integration**:
   - Each image is divided into chunks and stored as blocks in a blockchain.
   - The blockchain ensures data integrity and security.

4. **Thumbnail Generation**:
   - Thumbnails are generated for uploaded images for quick previews.
   - Private images are blurred for additional privacy.

5. **Image Viewer**:
   - Users can view high-resolution images with decryption keys.

6. **Responsive Design**:
   - The frontend is fully responsive and works seamlessly across devices.

---

## API Documentation
The backend API is built using FastAPI and provides endpoints for user authentication, image management, and blockchain operations. Below is an overview of the key API endpoints:

### **Authentication**
- **Register User**  
  `POST /register/uname`  
  Registers a new user and returns an authentication token.  
  **Request Body**:  
  ```json
  {
    "uname": "username"
  }# Pixel Lock - Secure Image Gallery

---

## Overview
Pixel Lock is a secure image gallery application that allows users to upload, encrypt, and view images with privacy and security in mind. The application leverages blockchain technology and IPFS (InterPlanetary File System) to securely store and manage images. It provides a seamless user experience with a React-based frontend and a FastAPI backend.

---

## Features
1. **User Authentication**:
   - Users can register and log in using a unique authentication token.
   - Authentication tokens are securely generated and stored.

2. **Image Upload**:
   - Users can upload images with optional privacy settings.
   - Images are encrypted before being stored.

3. **Blockchain Integration**:
   - Each image is divided into chunks and stored as blocks in a blockchain.
   - The blockchain ensures data integrity and security.

4. **Thumbnail Generation**:
   - Thumbnails are generated for uploaded images for quick previews.
   - Private images are blurred for additional privacy.

5. **Image Viewer**:
   - Users can view high-resolution images with decryption keys.

6. **Responsive Design**:
   - The frontend is fully responsive and works seamlessly across devices.

---

## Ports and Services
The application runs the following services on specific ports:

| **Service**       | **Description**                          | **Port** |
|--------------------|------------------------------------------|----------|
| **Frontend**       | React-based user interface              | `4000`   |
| **Backend**        | FastAPI server for API endpoints        | `10001`  |
| **IPFS API**       | IPFS node API for file storage          | `10002`  |
| **IPFS Gateway**   | IPFS gateway for accessing files        | `9080`   |

---

## API Overview
The backend API is built using FastAPI and provides the following key paths:

### **Authentication**
- `POST /register/uname`: Register a new user and generate an authentication token.
- `POST /login`: Authenticate a user and retrieve their thumbnails.

### **File Management**
- `POST /uploadFile/`: Upload an image file, encrypt it, and generate a thumbnail.
- `GET /file/{idx}`: Retrieve an image by its index in the blockchain.
- `POST /delete/{idx}`: Delete an image by its index in the blockchain.
- `GET /file`: Retrieve the total number of files and their thumbnails.

### **Utility**
- `GET /`: Check if the API is running.

---

## How to Run
1. **Prerequisites**:
   - Docker and Docker Compose installed on your system.

2. **Steps**:
   - Clone the repository.
   - Navigate to the project directory.
   - Run the following command to start all services:
     ```bash
     docker-compose up 
     ```
   - Access the services:
     - Frontend: [http://localhost:4000](http://localhost:4000)
     - Backend API: [http://localhost:10001](http://localhost:10001)
     - IPFS Gateway: [http://localhost:9080](http://localhost:9080)

---

## Technologies Used
- **Frontend**: React, Vite, Bootstrap
- **Backend**: FastAPI, Python
- **Storage**: Blockchain, IPFS
- **Image Processing**: PIL (Python Imaging Library)

---

## Future Enhancements
- Add support for video uploads.
- Implement multi-factor authentication.
- Enhance blockchain validation mechanisms.
- Add support for sharing images with other users.

---

## Contributors
- **Developer**: [Tanish]

Feel free to contribute to the project by submitting pull requests or reporting issues!
