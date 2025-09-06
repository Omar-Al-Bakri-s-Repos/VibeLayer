#!/usr/bin/env python3
"""
BMAD-Depot Integration Test
Test the complete integration between BMAD orchestrator and Depot sandboxes
"""
import sys
import json
import tempfile
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from bmad_depot_bridge import BMadDepotBridge

def create_test_story(temp_dir: Path, story_id: str = "test001") -> Path:
    """Create a test story file for integration testing"""
    story_content = f"""# Story: Test Integration Story - {story_id}

## Context
This is a test story created for validating the BMAD-Depot integration.
The story simulates a typical VibeLayer development task.

## Implementation Details
- Package: @vibelayer/test
- Technology: TypeScript, React
- Files to create: src/components/TestComponent.tsx

### Technical Requirements
- Create a new React component using TypeScript
- Follow VibeLayer coding conventions
- Use Tailwind CSS for styling

## Architecture Guidance
- Follow the existing component pattern in VibeLayer
- Use the shared utilities from @vibelayer/shared
- Implement proper TypeScript interfaces

## Acceptance Criteria
1. Component renders without errors
2. Component follows VibeLayer styling patterns
3. Component has proper TypeScript typing
4. Unit tests are included and passing

## Testing Requirements
- Unit tests with Jest
- Component testing with React Testing Library
- TypeScript compilation passes

## Dependencies
None - this is a standalone test story

## Priority
P1 - Critical for testing

## Story ID
{story_id}
"""
    
    story_file = temp_dir / f"story_{story_id}.md"
    story_file.write_text(story_content)
    return story_file

def test_depot_status():
    """Test 1: Verify Depot CLI is accessible"""
    print("🧪 Test 1: Depot CLI Status")
    
    bridge = BMadDepotBridge()
    result = bridge.validate_depot_status()
    
    print(f"   Status: {result['status']}")
    print(f"   Message: {result['message']}")
    
    if result['status'] == 'success':
        print("   ✅ PASS: Depot CLI is accessible")
        return True
    else:
        print("   ❌ FAIL: Depot CLI not accessible")
        return False

def test_story_validation():
    """Test 2: Story validation functionality"""
    print("\n🧪 Test 2: Story Validation")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test story
        story_file = create_test_story(temp_path, "validation_test")
        print(f"   Created test story: {story_file}")
        
        # Test validation
        bridge = BMadDepotBridge()
        result = bridge.validate_story_file(str(story_file))
        
        print(f"   Valid: {result['valid']}")
        print(f"   Story ID: {result['story_id']}")
        print(f"   Issues: {len(result['issues'])}")
        
        if result['issues']:
            for issue in result['issues']:
                print(f"     - {issue}")
        
        if result['valid']:
            print("   ✅ PASS: Story validation working")
            return True
        else:
            print("   ❌ FAIL: Story validation failed")
            return False

def test_session_management():
    """Test 3: Session management functionality"""
    print("\n🧪 Test 3: Session Management")
    
    bridge = BMadDepotBridge()
    
    # Test active sessions listing
    result = bridge.monitor_active_sessions(timeout_minutes=0)
    
    print(f"   Success: {result['success']}")
    print(f"   Active sessions: {result.get('active_sessions', {}).get('total_count', 0)}")
    
    if result['success']:
        print("   ✅ PASS: Session management working")
        return True
    else:
        print(f"   ❌ FAIL: Session management failed: {result.get('error', 'Unknown error')}")
        return False

def test_story_spawning_simulation():
    """Test 4: Simulate story spawning (without actual Depot execution)"""
    print("\n🧪 Test 4: Story Spawning Simulation")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test story
        story_file = create_test_story(temp_path, "spawn_test")
        
        bridge = BMadDepotBridge()
        
        # Validate story first
        validation = bridge.validate_story_file(str(story_file))
        if not validation['valid']:
            print("   ❌ FAIL: Test story validation failed")
            return False
        
        print(f"   Story validated: {validation['story_id']}")
        print("   📝 NOTE: Actual Depot spawning requires authentication")
        print("   📝 NOTE: This test validates the spawn preparation only")
        
        # Test would spawn here in real environment with:
        # result = bridge.spawn_development_agent(str(story_file))
        
        print("   ✅ PASS: Story spawn simulation completed")
        return True

def test_coordination_discovery():
    """Test 5: Story discovery for coordination"""
    print("\n🧪 Test 5: Story Discovery")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        stories_dir = temp_path / "stories"
        stories_dir.mkdir()
        
        # Create multiple test stories
        story1 = create_test_story(stories_dir, "coord001")
        story2 = create_test_story(stories_dir, "coord002") 
        story3 = create_test_story(stories_dir, "coord003")
        
        bridge = BMadDepotBridge()
        
        # Test story discovery
        stories = bridge.coordinator.discover_stories(str(stories_dir))
        
        print(f"   Stories discovered: {len(stories)}")
        for story in stories:
            print(f"     - {story['story_id']} (priority: {story['priority']})")
        
        if len(stories) == 3:
            print("   ✅ PASS: Story discovery working")
            return True
        else:
            print(f"   ❌ FAIL: Expected 3 stories, found {len(stories)}")
            return False

def run_integration_tests():
    """Run all integration tests"""
    print("🌉 BMAD-Depot Integration Test Suite")
    print("=" * 50)
    
    tests = [
        test_depot_status,
        test_story_validation,
        test_session_management,
        test_story_spawning_simulation,
        test_coordination_discovery
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"   💥 ERROR: Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"🏁 Integration Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All tests passed! BMAD-Depot integration is working.")
        return True
    else:
        print(f"❌ {total - passed} tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)