import React, { useState, useRef } from 'react';
import './imageviewer.css';
import { FaExpand, FaCompress, FaSync, FaPlay, FaPause, FaPlus, FaMinus } from 'react-icons/fa';

const ImageViewer = ({ src, alt }) => {
  const [zoomLevel, setZoomLevel] = useState(1);
  const [rotation, setRotation] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [intervalId, setIntervalId] = useState(null);
  const imageRef = useRef(null);

  const handleZoomIn = () => setZoomLevel((prev) => Math.min(prev + 0.1, 3));
  const handleZoomOut = () => setZoomLevel((prev) => Math.max(prev - 0.1, 0.5));
  const handleRotate = () => setRotation((prev) => (prev + 90) % 360);

  const toggleFullscreen = () => {
    if (!isFullscreen) {
      if (imageRef.current.requestFullscreen) {
        imageRef.current.requestFullscreen();
      }
      setIsFullscreen(true);
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
      setIsFullscreen(false);
    }
  };

  const startAutoplay = () => {
    if (isPlaying) return;
    const id = setInterval(() => setRotation((prev) => (prev + 90) % 360), 3000); // Rotate every 3 seconds
    setIntervalId(id);
    setIsPlaying(true);
  };

  const stopAutoplay = () => {
    clearInterval(intervalId);
    setIsPlaying(false);
  };

  return (
    <div className="image-viewer">
      <div
        ref={imageRef}
        className="image-viewer-image"
        style={{
          transform: `scale(${zoomLevel}) rotate(${rotation}deg)`,
        }}
      >
        <img src={src} alt={alt} draggable="false" />
      </div>

      <div className="image-viewer-controls">
        <button onClick={handleZoomIn}><FaPlus /></button>
        <button onClick={handleZoomOut}><FaMinus /></button>
        <button onClick={handleRotate}><FaSync /></button>
        <button onClick={toggleFullscreen}>{isFullscreen ? <FaCompress /> : <FaExpand />}</button>
        {/* {isPlaying ? (
          <button onClick={stopAutoplay}><FaPause /></button>
        ) : (
          <button onClick={startAutoplay}><FaPlay /></button>
        )} */}
      </div>
    </div>
  );
};

export default ImageViewer;

