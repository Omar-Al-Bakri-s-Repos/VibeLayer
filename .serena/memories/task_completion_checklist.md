# Task Completion Checklist

## Before Completing Any Development Task

### 1. Code Quality Checks
```bash
pnpm lint                   # Fix all linting issues
pnpm type-check             # Resolve all TypeScript errors
pnpm format                 # Format code consistently
```

### 2. Testing
```bash
pnpm test                   # Ensure all tests pass
# If tests are failing, investigate and fix issues
# Add new tests for new functionality
```

### 3. Build Verification
```bash
pnpm build                  # Ensure project builds successfully
# Check for build errors or warnings
# Verify all packages compile correctly
```

### 4. Development Server Check
```bash
pnpm dev                    # Start dev servers
# Verify the application starts without errors
# Test functionality in browser (control panel at localhost:3000)
# Check console for runtime errors
```

## Package-Specific Checks

### For Control Panel Changes
- Test authentication flows if auth-related changes
- Verify responsive design on different screen sizes
- Check accessibility with screen readers if UI changes
- Test PWA functionality if service worker changes

### For Shared Package Changes
- Run tests in packages that depend on shared
- Verify exports are correctly typed
- Check that breaking changes are documented

### For Mobile Changes (if applicable)
- Test on Android emulator/device
- Test on iOS simulator/device
- Verify graphics rendering performance

## Git Best Practices
- Commit messages should be clear and descriptive
- Keep commits atomic (one logical change per commit)
- Push to feature branch, not main directly
- Create pull request for review

## Documentation
- Update README.md if public API changes
- Add JSDoc comments for new public functions
- Update type definitions if interfaces change

## Performance Considerations
- Check bundle size impact for frontend changes
- Profile graphics rendering for overlay/effects changes
- Monitor memory usage for agent-related changes