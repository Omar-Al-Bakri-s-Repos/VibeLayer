#!/usr/bin/env python3
"""
BMAD-Depot Bridge Implementation
Python implementation to support the BMad Depot Bridge agent
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

# Add the depot scripts to path for imports
depot_scripts_path = Path(__file__).parent
sys.path.insert(0, str(depot_scripts_path))

from spawn_dev_agent import VibeLayerDevAgentSpawner
from session_coordinator import VibeLayerSessionCoordinator

class BMadDepotBridge:
    """
    Implementation bridge between BMAD orchestrator and Depot sandboxes
    Follows BMAD agent patterns while providing Python functionality
    """
    
    def __init__(self, project_root: str = "/home/omar/Documents/VibeLayer"):
        self.project_root = Path(project_root)
        self.spawner = VibeLayerDevAgentSpawner(str(project_root))
        self.coordinator = VibeLayerSessionCoordinator(str(project_root))
        
    def validate_depot_status(self) -> Dict:
        """Check if Depot CLI is installed and accessible"""
        try:
            import subprocess
            result = subprocess.run(
                ["depot", "--version"],
                capture_output=True,
                text=True,
                env={**os.environ, "PATH": f"/home/omar/.depot/bin:{os.environ.get('PATH', '')}"}
            )
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "version": result.stdout.strip(),
                    "message": "Depot CLI is installed and accessible"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Depot CLI not accessible: {result.stderr}"
                }
        except FileNotFoundError:
            return {
                "status": "error", 
                "message": "Depot CLI not found. Please install with: curl -L https://depot.dev/install-cli.sh | sh"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error checking Depot status: {str(e)}"
            }
    
    def validate_story_file(self, story_file_path: str) -> Dict:
        """
        Validate a story file for development agent spawning
        Following BMAD story requirements
        """
        story_path = Path(story_file_path)
        
        validation_result = {
            "valid": False,
            "story_id": None,
            "issues": [],
            "context_present": False,
            "dependencies": []
        }
        
        # Check file exists
        if not story_path.exists():
            validation_result["issues"].append(f"Story file not found: {story_file_path}")
            return validation_result
        
        try:
            content = story_path.read_text(encoding='utf-8')
            
            # Extract story ID
            story_id = story_path.stem.replace('story_', '').replace('.md', '')
            validation_result["story_id"] = story_id
            
            # Check for essential content sections
            required_sections = [
                ("## Context", "Story context and background"),
                ("## Implementation", "Implementation details"),
                ("## Acceptance Criteria", "Success criteria")
            ]
            
            for section, description in required_sections:
                if section.lower() not in content.lower():
                    validation_result["issues"].append(f"Missing {description} section: {section}")
                else:
                    validation_result["context_present"] = True
            
            # Extract dependencies
            if "depends on:" in content.lower():
                for line in content.split('\n'):
                    if line.lower().startswith('depends on:'):
                        deps_str = line.split(':', 1)[1].strip()
                        validation_result["dependencies"] = [d.strip() for d in deps_str.split(',') if d.strip()]
                        break
            
            # Check content length (stories should be substantial)
            if len(content.split('\n')) < 10:
                validation_result["issues"].append("Story appears too brief - may lack implementation context")
            
            # Check if dependencies are met (basic check)
            if validation_result["dependencies"]:
                # This would be enhanced to check actual story completion status
                validation_result["issues"].append(f"Dependencies found: {', '.join(validation_result['dependencies'])}")
            
            # Overall validation
            if len(validation_result["issues"]) == 0:
                validation_result["valid"] = True
            elif validation_result["context_present"] and len(validation_result["issues"]) <= 1:
                # Allow stories with minor issues if they have context
                validation_result["valid"] = True
                
        except Exception as e:
            validation_result["issues"].append(f"Error reading story file: {str(e)}")
        
        return validation_result
    
    def spawn_development_agent(self, story_file_path: str, story_id: str = None) -> Dict:
        """
        Spawn a development agent for a specific story
        Integrates with BMAD workflow patterns
        """
        # First validate the story
        validation = self.validate_story_file(story_file_path)
        
        if not validation["valid"]:
            return {
                "success": False,
                "error": "Story validation failed",
                "validation_issues": validation["issues"]
            }
        
        try:
            # Use the spawner to create the development agent
            session_data = self.spawner.spawn_development_agent(story_file_path, story_id)
            
            return {
                "success": True,
                "session_id": session_data["session_id"],
                "session_url": session_data.get("session_url"),
                "story_id": session_data["story_id"],
                "message": f"Development agent spawned for story: {session_data['story_id']}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to spawn development agent: {str(e)}"
            }
    
    def coordinate_parallel_development(self, stories_dir: str = None, max_concurrent: int = 5) -> Dict:
        """
        Coordinate parallel development of multiple stories
        Follows BMAD orchestration patterns
        """
        try:
            result = self.coordinator.coordinate_parallel_development(
                stories_dir=stories_dir,
                batch_size=max_concurrent
            )
            
            return {
                "success": True,
                "coordination_result": result,
                "message": f"Coordination completed. Spawned {result.get('sessions_spawned', 0)} sessions."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Coordination failed: {str(e)}"
            }
    
    def monitor_active_sessions(self, timeout_minutes: int = 30) -> Dict:
        """Monitor active development sessions"""
        try:
            # Get current session status
            active_sessions = self.spawner.list_active_sessions()
            
            if timeout_minutes > 0:
                # Start monitoring with timeout
                monitoring_result = self.coordinator.monitor_sessions(timeout_minutes)
                return {
                    "success": True,
                    "active_sessions": active_sessions,
                    "monitoring_result": monitoring_result,
                    "message": f"Monitoring completed after {monitoring_result.get('monitoring_duration_minutes', 0):.1f} minutes"
                }
            else:
                # Just return current status
                return {
                    "success": True,
                    "active_sessions": active_sessions,
                    "message": f"Found {active_sessions.get('total_count', 0)} active sessions"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Monitoring failed: {str(e)}"
            }
    
    def get_story_development_status(self, story_id: str) -> Dict:
        """Get development status for a specific story"""
        try:
            active_sessions = self.spawner.list_active_sessions()
            
            # Find session for this story
            story_session = None
            for session in active_sessions["active_sessions"]:
                if session["story_id"] == story_id:
                    story_session = session
                    break
            
            if story_session:
                # Get detailed session status
                detailed_status = self.spawner.get_session_status(story_session["session_id"])
                return {
                    "success": True,
                    "story_id": story_id,
                    "session_found": True,
                    "session_status": detailed_status,
                    "message": f"Story {story_id} status: {story_session['status']}"
                }
            else:
                return {
                    "success": True,
                    "story_id": story_id, 
                    "session_found": False,
                    "message": f"No active development session found for story: {story_id}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Status check failed: {str(e)}"
            }
    
    def cleanup_old_sessions(self, days_old: int = 7) -> Dict:
        """Clean up old session files"""
        try:
            result = self.coordinator.cleanup_old_sessions(days_old)
            return {
                "success": True,
                "cleanup_result": result,
                "message": f"Cleaned up {result.get('cleaned_files', 0)} old session files"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Cleanup failed: {str(e)}"
            }

def main():
    """CLI interface for BMAD-Depot Bridge"""
    import argparse
    
    parser = argparse.ArgumentParser(description="BMAD-Depot Bridge - Coordinate development agents")
    parser.add_argument("command", help="Command to execute", choices=[
        "depot-status", "spawn-dev", "coordinate", "monitor", "story-status", "cleanup", "validate-story"
    ])
    parser.add_argument("--story-file", help="Path to story file")
    parser.add_argument("--story-id", help="Story identifier")
    parser.add_argument("--stories-dir", help="Directory containing story files") 
    parser.add_argument("--max-concurrent", type=int, default=5, help="Maximum concurrent sessions")
    parser.add_argument("--timeout", type=int, default=30, help="Monitoring timeout in minutes")
    parser.add_argument("--days-old", type=int, default=7, help="Clean up files older than N days")
    
    args = parser.parse_args()
    
    bridge = BMadDepotBridge()
    
    if args.command == "depot-status":
        result = bridge.validate_depot_status()
    elif args.command == "spawn-dev":
        if not args.story_file:
            print("Error: --story-file required for spawn-dev command")
            sys.exit(1)
        result = bridge.spawn_development_agent(args.story_file, args.story_id)
    elif args.command == "coordinate":
        result = bridge.coordinate_parallel_development(args.stories_dir, args.max_concurrent)
    elif args.command == "monitor":
        result = bridge.monitor_active_sessions(args.timeout)
    elif args.command == "story-status":
        if not args.story_id:
            print("Error: --story-id required for story-status command")
            sys.exit(1)
        result = bridge.get_story_development_status(args.story_id)
    elif args.command == "cleanup":
        result = bridge.cleanup_old_sessions(args.days_old)
    elif args.command == "validate-story":
        if not args.story_file:
            print("Error: --story-file required for validate-story command")
            sys.exit(1)
        result = bridge.validate_story_file(args.story_file)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()