'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Mic, MicOff, AlertTriangle, CheckCircle } from 'lucide-react';

interface MicrophonePermissionProps {
  onPermissionGranted?: () => void;
  onPermissionDenied?: () => void;
}

export function MicrophonePermission({ onPermissionGranted, onPermissionDenied }: MicrophonePermissionProps) {
  const [permissionState, setPermissionState] = useState<'unknown' | 'granted' | 'denied' | 'requesting'>('unknown');
  const [error, setError] = useState<string>('');

  useEffect(() => {
    checkPermissionStatus();
  }, []);

  const checkPermissionStatus = async () => {
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        setError('Microphone access is not supported in this browser');
        return;
      }

      // Check current permission status
      const permission = await navigator.permissions.query({ name: 'microphone' as PermissionName });
      
      if (permission.state === 'granted') {
        setPermissionState('granted');
        onPermissionGranted?.();
      } else if (permission.state === 'denied') {
        setPermissionState('denied');
        onPermissionDenied?.();
      } else {
        setPermissionState('unknown');
      }

      // Listen for permission changes
      permission.onchange = () => {
        if (permission.state === 'granted') {
          setPermissionState('granted');
          onPermissionGranted?.();
        } else if (permission.state === 'denied') {
          setPermissionState('denied');
          onPermissionDenied?.();
        }
      };
    } catch (err) {
      console.warn('Permission query not supported, will request directly');
      setPermissionState('unknown');
    }
  };

  const requestMicrophoneAccess = async () => {
    setPermissionState('requesting');
    setError('');

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        }
      });
      
      // Stop the stream immediately as we only need permission
      stream.getTracks().forEach(track => track.stop());
      
      setPermissionState('granted');
      onPermissionGranted?.();
    } catch (err) {
      setPermissionState('denied');
      
      if (err instanceof Error) {
        if (err.name === 'NotAllowedError') {
          setError('Microphone access denied. Please allow microphone access in your browser settings.');
        } else if (err.name === 'NotFoundError') {
          setError('No microphone found. Please connect a microphone and try again.');
        } else {
          setError(`Error accessing microphone: ${err.message}`);
        }
      } else {
        setError('Failed to access microphone. Please check your browser settings.');
      }
      
      onPermissionDenied?.();
    }
  };

  const renderContent = () => {
    switch (permissionState) {
      case 'granted':
        return (
          <div className="text-center space-y-4">
            <div className="flex justify-center">
              <CheckCircle className="h-12 w-12 text-green-500" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-green-700">Microphone Access Granted</h3>
              <p className="text-gray-600">VibeLayer can now listen for voice commands and audio cues.</p>
            </div>
          </div>
        );

      case 'denied':
        return (
          <div className="text-center space-y-4">
            <div className="flex justify-center">
              <MicOff className="h-12 w-12 text-red-500" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-red-700">Microphone Access Denied</h3>
              <p className="text-gray-600">To use voice features, please enable microphone access in your browser settings.</p>
            </div>
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-3">
                <div className="flex items-center gap-2 text-red-800 text-sm">
                  <AlertTriangle className="h-4 w-4" />
                  {error}
                </div>
              </div>
            )}
            <Button onClick={requestMicrophoneAccess} variant="outline">
              Try Again
            </Button>
          </div>
        );

      case 'requesting':
        return (
          <div className="text-center space-y-4">
            <div className="flex justify-center">
              <Mic className="h-12 w-12 text-blue-500 animate-pulse" />
            </div>
            <div>
              <h3 className="text-lg font-semibold">Requesting Microphone Access</h3>
              <p className="text-gray-600">Please allow microphone access when prompted by your browser.</p>
            </div>
          </div>
        );

      default:
        return (
          <div className="text-center space-y-4">
            <div className="flex justify-center">
              <Mic className="h-12 w-12 text-gray-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold">Microphone Access Required</h3>
              <p className="text-gray-600">
                VibeLayer uses your microphone to detect voice commands and audio cues for triggering visual effects.
              </p>
            </div>
            <Button onClick={requestMicrophoneAccess} className="bg-blue-600 hover:bg-blue-700">
              <Mic className="mr-2 h-4 w-4" />
              Allow Microphone Access
            </Button>
          </div>
        );
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Audio Permissions</CardTitle>
        <CardDescription>
          Enable microphone access for voice-controlled effects
        </CardDescription>
      </CardHeader>
      <CardContent>
        {renderContent()}
      </CardContent>
    </Card>
  );
}