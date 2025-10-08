# Frontend Testing Guide

This document provides information on how to run and write tests for the frontend application.

## Running Tests

You can run the tests using the following commands:

```bash
# Run tests in watch mode (default)
npm test

# Run tests once with coverage report
npm test -- --coverage --watchAll=false

# Run a specific test file
npm test -- ChatInput.test.tsx
```

## Test Structure

Tests are organized in `__tests__` directories next to the components they test. For example:

```
src/
  components/
    Logo.tsx
    __tests__/
      Logo.test.tsx
```

## Components Tested

The following components have tests:

1. **Logo** - Tests rendering with different sizes and CSS classes
2. **Sidebar** - Tests rendering with and without chats, chat selection, and new chat button
3. **ChatMessage** - Tests rendering of user and bot messages, including markdown support
4. **ChatInput** - Tests input field, button rendering, and form submission
5. **ChatHistory** - Tests empty state and rendering of multiple messages
6. **App** - Tests the main application flow, including creating chats and sending messages

## API Service Tests

The API service tests verify:
- Sending messages to the API
- Handling API errors
- Handling network errors

## Troubleshooting Common Test Issues

### 1. Issues with React Hooks in Mock Components

When mocking components that use React hooks, avoid using hooks directly in the mock factory function. Instead, create a separate component function:

```javascript
// WRONG:
jest.mock('../Component', () => {
  return () => {
    const [state, setState] = React.useState(''); // This will fail
    return <div>{state}</div>;
  };
});

// CORRECT:
jest.mock('../Component', () => {
  const MockComponent = (props) => {
    // Use hooks here
    return <div>{props.value}</div>;
  };
  return MockComponent;
});
```

### 2. Issues with Document References

Don't use `document` directly in mock functions. Instead, use refs or test utilities:

```javascript
// WRONG:
jest.mock('../Component', () => {
  return () => {
    const handleClick = () => {
      const element = document.querySelector('.some-class'); // This will fail
    };
    return <button onClick={handleClick}>Click</button>;
  };
});

// CORRECT:
jest.mock('../Component', () => {
  const MockComponent = () => {
    const ref = React.useRef(null);
    const handleClick = () => {
      if (ref.current) {
        // Do something with ref
      }
    };
    return <button ref={ref} onClick={handleClick}>Click</button>;
  };
  return MockComponent;
});
```

### 3. Issues with Environment Variables

Testing code that relies on environment variables can be tricky. Consider:

- Using a default value in your code: `process.env.VARIABLE || 'default'`
- Mocking the entire module that uses the environment variable
- Using Jest's `jest.mock()` to mock specific modules

## Best Practices

1. **Test Component Rendering**: Verify that components render correctly with different props
2. **Test User Interactions**: Test what happens when users click buttons or enter text
3. **Test Error States**: Verify that components handle errors gracefully
4. **Mock External Dependencies**: Use Jest's mocking capabilities to isolate components
5. **Keep Tests Simple**: Each test should verify one specific behavior