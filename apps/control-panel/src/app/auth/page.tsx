'use client';

import { useState } from 'react';
import { SignupForm } from '@/components/auth/SignupForm';
import { LoginForm } from '@/components/auth/LoginForm';
import { MicrophonePermission } from '@/components/microphone/MicrophonePermission';

export default function AuthPage() {
  const [mode, setMode] = useState<'login' | 'signup'>('login');
  const [showMicPermission, setShowMicPermission] = useState(false);

  const toggleMode = () => {
    setMode(mode === 'login' ? 'signup' : 'login');
  };

  const handleAuthSuccess = () => {
    setShowMicPermission(true);
  };

  const handlePermissionGranted = () => {
    // Redirect to dashboard
    window.location.href = '/dashboard';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        {!showMicPermission ? (
          <>
            <div className="text-center">
              <h1 className="text-3xl font-bold text-white mb-2">VibeLayer</h1>
              <p className="text-purple-200">AI-powered visual effects platform</p>
            </div>
            
            {mode === 'login' ? (
              <LoginForm onToggleMode={toggleMode} />
            ) : (
              <SignupForm onToggleMode={toggleMode} />
            )}
          </>
        ) : (
          <MicrophonePermission 
            onPermissionGranted={handlePermissionGranted}
            onPermissionDenied={() => {
              // Still allow access but show warning
              setTimeout(() => window.location.href = '/dashboard', 2000);
            }}
          />
        )}
      </div>
    </div>
  );
}