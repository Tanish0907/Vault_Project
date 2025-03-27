import React, { useState } from 'react';
import LightGallery from 'lightgallery/react';
import 'lightgallery/css/lightgallery.css';
import 'lightgallery/css/lg-thumbnail.css';
import 'lightgallery/css/lg-autoplay.css';
import 'lightgallery/css/lg-fullscreen.css';
import 'lightgallery/css/lg-rotate.css';
import lgThumbnail from 'lightgallery/plugins/thumbnail';
import lgAutoplay from 'lightgallery/plugins/autoplay';
import lgFullscreen from 'lightgallery/plugins/fullscreen';
import lgRotate from 'lightgallery/plugins/rotate';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import ImageViewer from './ImageViewer'; // Import the ImageViewer component
import './Gallery.css';
import { FiUpload } from 'react-icons/fi'; // Add this import for icons

export const Gallery = ({ imageList }) => {
  const [images, setImages] = useState(imageList);
  const [username, setUsername] = useState('');
  const [encToken, setEncToken] = useState('');
  const [authToken, setAuthToken] = useState('');
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showCredentialsModal, setShowCredentialsModal] = useState(false);
  const [showImageViewerModal, setShowImageViewerModal] = useState(false);
  const [selectedImageIndex, setSelectedImageIndex] = useState(null);
  const [currentImage, setCurrentImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [checked, setChecked] = useState(false);

  // Open and close upload modal
  const handleCloseUploadModal = () => setShowUploadModal(false);
  const handleShowUploadModal = () => setShowUploadModal(true);
  
  // Close credentials modal
  const handleCloseCredentialsModal = () => setShowCredentialsModal(false);

  // Close image viewer modal
  const handleCloseImageViewerModal = () => {
    setShowImageViewerModal(false);
    setCurrentImage(null); // Clear current image when modal closes
  };

  // Handle file upload
  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('enc_tocken', encToken);  // Corrected to match the API parameter
    formData.append('uname', username);
    formData.append('auth_token', authToken);
    formData.append('privacy', checked ? 'true' : 'false'); // Send as a boolean string

    //console.log(...formData); // Log formData to verify its contents

    try {
      const response = await axios.post(
        'http://localhost:8000/uploadFile/', 
        formData, 
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      const newThumbnail = {
        src: `data:image/jpg;base64,${response.data}`,
        alt: file.name
      };

      setImages((prevImages) => [...prevImages, newThumbnail]);
    } catch (error) {
      console.error('File upload failed:', error.response || error);
    }
  };

  // Open credentials modal on thumbnail click
  const handleThumbnailClick = (index) => {
    setSelectedImageIndex(index + 1); // Set the 1-based index for the API call
    setShowCredentialsModal(true);    // Show credentials modal
  };

  // Fetch high-resolution image after user provides credentials
  const fetchHighResolutionImage = async () => {
    if (!selectedImageIndex || !username || !authToken || !encToken) return;

    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/file/${selectedImageIndex}`, {
        params: { k: encToken, uname: username, auth_token: authToken }
      });

      setCurrentImage(`data:image/jpg;base64,${response.data.img}`);
      setShowImageViewerModal(true); // Show the ImageViewer modal after fetching
    } catch (error) {
      console.error('Failed to fetch high-resolution image:', error.response || error);
    } finally {
      setLoading(false);
      setShowCredentialsModal(false);  // Close credentials modal after API call
    }
  };

  return (
    <div className="gallery-container">
      <div className="gallery-header">
        <h1 className="gallery-title">Gallery</h1>
        <button className="upload-button" onClick={handleShowUploadModal}>
          <FiUpload />
          Upload Image
        </button>
      </div>
      
      {/* Upload Modal */}
      <Modal 
        show={showUploadModal} 
        onHide={handleCloseUploadModal}
        className="custom-modal"
      >
        <Modal.Header closeButton>
          <Modal.Title>Upload Image</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <input
            type="text"
            className="form-control"
            placeholder="Enter Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="text"
            className="form-control"
            placeholder="Enter Encryption Token"
            value={encToken}
            onChange={(e) => setEncToken(e.target.value)}
          />
          <input
            type="text"
            className="form-control"
            placeholder="Enter Auth Token"
            value={authToken}
            onChange={(e) => setAuthToken(e.target.value)}
          />
          <div className="checkbox-container">
            <input
              type="checkbox"
              id="privacy-checkbox"
              checked={checked}
              onChange={(event) => setChecked(event.target.checked)}
            />
            <label htmlFor="privacy-checkbox">Private Image</label>
          </div>
          <input
            className="form-control"
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            disabled={!username || !encToken || !authToken}
          />
        </Modal.Body>
      </Modal>

      {/* Flexbox Gallery */}
      <div className="gallery-flex">
        <LightGallery 
          elementClassNames="gallery-flex"
          onInit={() => console.log('LightGallery initialized')} 
          speed={500} 
          plugins={[lgThumbnail]}
          download={false}
        >
          {images.map((image, index) => (
            <a 
              className="image-container"
              href={image.src} 
              key={index}
              onClick={(e) => {
                e.preventDefault();
                handleThumbnailClick(index);
              }}
            >
              <img
                alt={image.alt}
                src={image.src}
                onContextMenu={(e) => e.preventDefault()}
                draggable="false"
              />
            </a>
          ))}
        </LightGallery>
      </div>

      {loading && (
        <div className="loading-indicator">
          Loading high-resolution image...
        </div>
      )}

      {/* Credentials Modal for High-Res Image Fetch */}
      <Modal show={showCredentialsModal} onHide={handleCloseCredentialsModal} className="custom-modal">
        <Modal.Header closeButton>
          <Modal.Title>Enter Credentials</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <input
            type="text"
            className="form-control"
            placeholder="Enter Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="text"
            className="form-control"
            placeholder="Enter Key (Encryption Token)"
            value={encToken}
            onChange={(e) => setEncToken(e.target.value)}
          />
          <input
            type="text"
            className="form-control"
            placeholder="Enter Auth Token"
            value={authToken}
            onChange={(e) => setAuthToken(e.target.value)}
          />
          <div className="checkbox-container">
            <input
              type="checkbox"
              id="privacy-checkbox"
              checked={checked}
              onChange={(event) => setChecked(event.target.checked)}
            />
            <label htmlFor="privacy-checkbox">Private Image</label>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseCredentialsModal}>
            Cancel
          </Button>
          <Button 
            variant="primary" 
            onClick={fetchHighResolutionImage}
            disabled={!username || !encToken || !authToken}
          >
            Fetch Image
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Image Viewer Modal */}
      <Modal show={showImageViewerModal} onHide={handleCloseImageViewerModal} size="lg" centered className="custom-modal">
        <Modal.Header closeButton>
          <Modal.Title>Image Viewer</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {currentImage && <ImageViewer src={currentImage} alt="High-resolution view" />}
        </Modal.Body>
      </Modal>
    </div>
  );
};

export default Gallery;

