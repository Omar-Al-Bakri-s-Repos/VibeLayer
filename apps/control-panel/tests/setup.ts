import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock Web APIs that are not available in jsdom
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock navigator.permissions
Object.defineProperty(navigator, 'permissions', {
  writable: true,
  value: {
    query: vi.fn().mockResolvedValue({
      state: 'prompt',
      onchange: null,
    }),
  },
});

// Mock navigator.mediaDevices
Object.defineProperty(navigator, 'mediaDevices', {
  writable: true,
  value: {
    getUserMedia: vi.fn(),
  },
});

// Mock crypto.randomUUID
Object.defineProperty(crypto, 'randomUUID', {
  writable: true,
  value: vi.fn(() => '12345678-1234-1234-1234-123456789012'),
});