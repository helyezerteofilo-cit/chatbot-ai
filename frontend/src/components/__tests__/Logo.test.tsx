import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Logo from '../Logo';

describe('Logo Component', () => {
  test('renders with default medium size', () => {
    render(<Logo />);
    const logoElement = screen.getByAltText('AI Chatbot Logo');
    expect(logoElement).toBeInTheDocument();
    expect(logoElement.parentElement).toHaveClass('logo-medium');
  });

  test('renders with small size when specified', () => {
    render(<Logo size="small" />);
    const logoElement = screen.getByAltText('AI Chatbot Logo');
    expect(logoElement).toBeInTheDocument();
    expect(logoElement.parentElement).toHaveClass('logo-small');
  });

  test('renders with large size when specified', () => {
    render(<Logo size="large" />);
    const logoElement = screen.getByAltText('AI Chatbot Logo');
    expect(logoElement).toBeInTheDocument();
    expect(logoElement.parentElement).toHaveClass('logo-large');
  });

  test('has correct CSS classes', () => {
    render(<Logo />);
    const logoContainer = screen.getByAltText('AI Chatbot Logo').parentElement;
    expect(logoContainer).toHaveClass('logo');
    expect(logoContainer).toHaveClass('logo-medium');
  });

  test('image has logo-image class', () => {
    render(<Logo />);
    const logoImage = screen.getByAltText('AI Chatbot Logo');
    expect(logoImage).toHaveClass('logo-image');
  });
});