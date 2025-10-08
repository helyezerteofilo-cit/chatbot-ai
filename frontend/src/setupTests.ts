// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

// Mock the image imports
jest.mock('./assets/logo.png', () => 'logo-mock.png');

// Mock for ResizeObserver which is not available in Jest environment
global.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Mock for scrollIntoView which is not available in Jest environment
Element.prototype.scrollIntoView = jest.fn();

// Mock for window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // Deprecated
    removeListener: jest.fn(), // Deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Suppress specific console errors during tests
const originalError = console.error;
console.error = (...args) => {
  // Don't log React warnings and specific test-related errors
  if (
    /Warning:/.test(args[0]) || 
    /Error sending message:/.test(args[0]) ||
    /Test was not wrapped in act/.test(args[0])
  ) {
    return;
  }
  originalError(...args);
};