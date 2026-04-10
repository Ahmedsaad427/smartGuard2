import React, { useState, useEffect, useRef, useCallback } from 'react';
import '../styles/BrowserCamera.css';

const BrowserCamera = ({ onCameraStatusChange, onDetectionResult }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const animationRef = useRef(null);
  
  const [isStreaming, setIsStreaming] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [detectionResults, setDetectionResults] = useState([]);
  const [cameraPermission, setCameraPermission] = useState('prompted'); // 'prompted', 'granted', 'denied'

  // Start camera stream
  const startCamera = useCallback(async () => {
    try {
      setError('');
      setCameraPermission('prompted');
      
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user'
        } 
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsStreaming(true);
        setCameraPermission('granted');
        onCameraStatusChange?.('online');
        
        console.log('Camera started successfully');
      }
    } catch (err) {
      console.error('Camera access error:', err);
      setError('Cannot access camera. Please ensure camera permissions are granted.');
      setCameraPermission('denied');
      onCameraStatusChange?.('offline');
      setIsStreaming(false);
    }
  }, [onCameraStatusChange]);

  // Stop camera stream
  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
      animationRef.current = null;
    }
    
    setIsStreaming(false);
    setIsProcessing(false);
    onCameraStatusChange?.('offline');
    console.log('Camera stopped');
  }, [onCameraStatusChange]);

  // Simulate detection processing
  const processFrame = useCallback(() => {
    if (!videoRef.current || !canvasRef.current || !isStreaming) return;
    
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Set canvas size to match video
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    
    // Draw current frame to canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Simulate detection (in real app, this would send frame to backend)
    if (Math.random() < 0.02) { // 2% chance of detection for demo
      const detection = {
        id: Date.now(),
        type: ['suspicious_behavior', 'unauthorized_access', 'loitering'][Math.floor(Math.random() * 3)],
        confidence: Math.random() * 0.3 + 0.7, // 70-100% confidence
        timestamp: new Date().toISOString(),
        location: 'Camera 1'
      };
      
      setDetectionResults(prev => [detection, ...prev.slice(0, 4)]);
      onDetectionResult?.(detection);
    }
    
    // Continue processing
    animationRef.current = requestAnimationFrame(processFrame);
  }, [isStreaming, onDetectionResult]);

  // Start processing when streaming begins
  useEffect(() => {
    if (isStreaming && !isProcessing) {
      setIsProcessing(true);
      processFrame();
    } else if (!isStreaming && isProcessing) {
      setIsProcessing(false);
    }
  }, [isStreaming, isProcessing, processFrame]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, [stopCamera]);

  // Auto-start camera on mount
  useEffect(() => {
    startCamera();
  }, [startCamera]);

  return (
    <div className="browser-camera">
      <div className="camera-header">
        <h3>Live Camera Feed</h3>
        <div className="camera-controls">
          <button 
            onClick={isStreaming ? stopCamera : startCamera}
            className={`camera-btn ${isStreaming ? 'stop' : 'start'}`}
          >
            {isStreaming ? 'Stop Camera' : 'Start Camera'}
          </button>
          <span className={`camera-status ${isStreaming ? 'online' : 'offline'}`}>
            {isStreaming ? 'Online' : 'Offline'}
          </span>
        </div>
      </div>
      
      {error && (
        <div className="camera-error">
          {error}
        </div>
      )}
      
      <div className="camera-container">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="camera-video"
          style={{ display: isStreaming ? 'block' : 'none' }}
        />
        
        {!isStreaming && !error && (
          <div className="camera-placeholder">
            <div className="placeholder-icon">Camera</div>
            <p>Click "Start Camera" to begin monitoring</p>
            <small>Make sure to allow camera permissions when prompted</small>
          </div>
        )}
        
        <canvas
          ref={canvasRef}
          className="camera-canvas"
          style={{ display: 'none' }}
        />
      </div>
      
      {detectionResults.length > 0 && (
        <div className="detection-results">
          <h4>Recent Detections</h4>
          <div className="detection-list">
            {detectionResults.map(detection => (
              <div key={detection.id} className="detection-item">
                <span className="detection-type">{detection.type}</span>
                <span className="detection-confidence">
                  {Math.round(detection.confidence * 100)}%
                </span>
                <span className="detection-time">
                  {new Date(detection.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default BrowserCamera;
