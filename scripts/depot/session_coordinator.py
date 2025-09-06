#!/usr/bin/env python3
"""
VibeLayer Session Coordinator
Manages multiple concurrent development agent sessions and coordinates parallel development work.
"""
import os
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from spawn_dev_agent import VibeLayerDevAgentSpawner

class VibeLayerSessionCoordinator:
    def __init__(self, project_root: str = "/home/omar/Documents/VibeLayer", max_concurrent: int = 10):
        self.project_root = Path(project_root)
        self.session_store = self.project_root / ".depot/sessions"
        self.artifacts_dir = self.project_root / ".depot/artifacts"
        self.max_concurrent = max_concurrent
        self.spawner = VibeLayerDevAgentSpawner(project_root)
        
        # Ensure directories exist
        self.session_store.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        
        # Thread lock for session management
        self._lock = threading.Lock()
    
    def discover_stories(self, stories_dir: str = None) -> List[Dict]:
        """
        Discover all available story files for development
        
        Args:
            stories_dir: Directory containing story files (auto-discover if None)
            
        Returns:
            List of story metadata dictionaries
        """
        if stories_dir is None:
            # Look for stories in common BMAD locations
            possible_dirs = [
                self.project_root / ".bmad/stories",
                self.project_root / "stories", 
                self.project_root / ".bmad/artifacts/stories"
            ]
            
            for dir_path in possible_dirs:
                if dir_path.exists():
                    stories_dir = str(dir_path)
                    break
            
            if not stories_dir:
                print("❌ No stories directory found. Expected locations:")
                for dir_path in possible_dirs:
                    print(f"   - {dir_path}")
                return []
        
        stories_path = Path(stories_dir)
        if not stories_path.exists():
            print(f"❌ Stories directory not found: {stories_dir}")
            return []
        
        stories = []
        for story_file in stories_path.glob("*.md"):
            try:
                content = story_file.read_text(encoding='utf-8')
                
                # Extract story metadata
                story_id = story_file.stem.replace('story_', '')
                
                # Look for priority in story content
                priority = 5  # default
                if "priority:" in content.lower():
                    for line in content.split('\n'):
                        if line.lower().startswith('priority:'):
                            try:
                                priority = int(line.split(':')[1].strip())
                            except:
                                priority = 5
                            break
                
                # Look for dependencies
                dependencies = []
                if "depends on:" in content.lower():
                    for line in content.split('\n'):
                        if line.lower().startswith('depends on:'):
                            deps_str = line.split(':', 1)[1].strip()
                            dependencies = [d.strip() for d in deps_str.split(',') if d.strip()]
                            break
                
                stories.append({
                    "story_id": story_id,
                    "file_path": str(story_file),
                    "priority": priority,
                    "dependencies": dependencies,
                    "size_estimate": len(content.split('\n'))  # rough complexity
                })
                
            except Exception as e:
                print(f"⚠️  Warning: Could not process story file {story_file}: {e}")
                continue
        
        # Sort by priority (lower number = higher priority)
        stories.sort(key=lambda x: (x['priority'], x['story_id']))
        
        print(f"📚 Discovered {len(stories)} stories for development")
        return stories
    
    def get_ready_stories(self, stories: List[Dict]) -> List[Dict]:
        """
        Filter stories that are ready for development (dependencies met)
        """
        # Get completed story IDs
        completed_stories = set()
        active_sessions = self.spawner.list_active_sessions()
        
        for session in active_sessions["active_sessions"]:
            if session["status"] == "completed":
                completed_stories.add(session["story_id"])
        
        ready_stories = []
        for story in stories:
            # Check if all dependencies are completed
            if all(dep in completed_stories for dep in story["dependencies"]):
                # Check if not already in progress
                story_in_progress = any(
                    session["story_id"] == story["story_id"] and session["status"] in ["running"]
                    for session in active_sessions["active_sessions"]
                )
                
                if not story_in_progress:
                    ready_stories.append(story)
        
        return ready_stories
    
    def coordinate_parallel_development(self, stories_dir: str = None, batch_size: int = None) -> Dict:
        """
        Coordinate parallel development of multiple stories
        
        Args:
            stories_dir: Directory containing story files
            batch_size: Maximum number of concurrent sessions (uses max_concurrent if None)
            
        Returns:
            Summary of coordination results
        """
        if batch_size is None:
            batch_size = self.max_concurrent
        
        print(f"🚀 Starting parallel development coordination (max {batch_size} concurrent)")
        
        # Discover available stories
        all_stories = self.discover_stories(stories_dir)
        if not all_stories:
            return {"error": "No stories found for development", "stories_processed": 0}
        
        coordination_results = {
            "total_stories": len(all_stories),
            "sessions_spawned": 0,
            "sessions_completed": 0,
            "sessions_failed": 0,
            "errors": []
        }
        
        # Process stories in batches
        remaining_stories = all_stories.copy()
        
        while remaining_stories:
            # Get stories ready for development
            ready_stories = self.get_ready_stories(remaining_stories)
            
            if not ready_stories:
                # Check if we have any running sessions
                active_sessions = self.spawner.list_active_sessions()
                running_count = sum(1 for s in active_sessions["active_sessions"] if s["status"] == "running")
                
                if running_count == 0:
                    print("📋 No more stories ready and no sessions running. Coordination complete.")
                    break
                else:
                    print(f"⏳ Waiting for {running_count} running sessions to complete dependencies...")
                    time.sleep(30)  # Wait before checking again
                    continue
            
            # Spawn sessions for ready stories (up to batch_size)
            batch = ready_stories[:batch_size]
            print(f"📦 Processing batch of {len(batch)} stories")
            
            # Spawn development agents in parallel
            with ThreadPoolExecutor(max_workers=batch_size) as executor:
                # Submit all story processing tasks
                future_to_story = {}
                for story in batch:
                    future = executor.submit(self._process_story_safe, story)
                    future_to_story[future] = story
                
                # Process completed tasks
                for future in as_completed(future_to_story):
                    story = future_to_story[future]
                    try:
                        result = future.result()
                        if result["success"]:
                            coordination_results["sessions_spawned"] += 1
                            print(f"✅ Session spawned for story: {story['story_id']}")
                        else:
                            coordination_results["sessions_failed"] += 1
                            coordination_results["errors"].append(f"Story {story['story_id']}: {result['error']}")
                            print(f"❌ Failed to spawn session for story: {story['story_id']}")
                    except Exception as e:
                        coordination_results["sessions_failed"] += 1
                        coordination_results["errors"].append(f"Story {story['story_id']}: {str(e)}")
                        print(f"💥 Unexpected error for story {story['story_id']}: {e}")
            
            # Remove processed stories from remaining list
            processed_ids = {story['story_id'] for story in batch}
            remaining_stories = [s for s in remaining_stories if s['story_id'] not in processed_ids]
            
            # Brief pause between batches
            if remaining_stories:
                time.sleep(5)
        
        print(f"🎉 Coordination complete. Spawned {coordination_results['sessions_spawned']} sessions.")
        return coordination_results
    
    def _process_story_safe(self, story: Dict) -> Dict:
        """Safely process a single story with error handling"""
        try:
            session_data = self.spawner.spawn_development_agent(
                story_file_path=story["file_path"],
                story_id=story["story_id"]
            )
            return {"success": True, "session_data": session_data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def monitor_sessions(self, timeout_minutes: int = 60) -> Dict:
        """
        Monitor active development sessions and report status
        
        Args:
            timeout_minutes: How long to monitor before timing out
            
        Returns:
            Monitoring summary
        """
        start_time = datetime.utcnow()
        timeout_time = start_time + timedelta(minutes=timeout_minutes)
        
        print(f"📊 Monitoring development sessions (timeout: {timeout_minutes} min)")
        
        monitoring_results = {
            "monitoring_duration_minutes": 0,
            "sessions_completed": 0,
            "sessions_failed": 0,
            "sessions_timeout": 0,
            "final_status": {}
        }
        
        while datetime.utcnow() < timeout_time:
            active_sessions = self.spawner.list_active_sessions()
            
            running_sessions = [s for s in active_sessions["active_sessions"] if s["status"] == "running"]
            
            if not running_sessions:
                print("✅ All sessions completed or no active sessions")
                break
            
            print(f"⏳ Monitoring {len(running_sessions)} active sessions...")
            for session in running_sessions[:5]:  # Show first 5
                print(f"   - {session['story_id']}: {session['status']} (started: {session['started_at']})")
            
            if len(running_sessions) > 5:
                print(f"   ... and {len(running_sessions) - 5} more")
            
            time.sleep(30)  # Check every 30 seconds
        
        # Final status
        final_sessions = self.spawner.list_active_sessions()
        monitoring_results["monitoring_duration_minutes"] = (datetime.utcnow() - start_time).total_seconds() / 60
        monitoring_results["final_status"] = final_sessions
        
        print(f"📊 Monitoring completed after {monitoring_results['monitoring_duration_minutes']:.1f} minutes")
        return monitoring_results
    
    def cleanup_old_sessions(self, days_old: int = 7) -> Dict:
        """Clean up session files older than specified days"""
        cutoff_time = datetime.utcnow() - timedelta(days=days_old)
        
        cleaned = 0
        for session_file in self.session_store.glob("*.json"):
            try:
                session_data = json.loads(session_file.read_text())
                session_time = datetime.fromisoformat(session_data["started_at"].replace('Z', '+00:00'))
                
                if session_time < cutoff_time:
                    session_file.unlink()
                    cleaned += 1
                    
            except (json.JSONDecodeError, KeyError, ValueError):
                # Remove corrupted session files
                session_file.unlink()
                cleaned += 1
        
        print(f"🧹 Cleaned up {cleaned} old session files")
        return {"cleaned_files": cleaned}

def main():
    """CLI interface for session coordinator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Coordinate BMAD development agent sessions")
    parser.add_argument("--stories-dir", help="Directory containing story files")
    parser.add_argument("--max-concurrent", type=int, default=10, help="Maximum concurrent sessions")
    parser.add_argument("--coordinate", action="store_true", help="Start coordination of parallel development")
    parser.add_argument("--monitor", action="store_true", help="Monitor active sessions")
    parser.add_argument("--monitor-timeout", type=int, default=60, help="Monitoring timeout in minutes")
    parser.add_argument("--cleanup", action="store_true", help="Clean up old session files")
    parser.add_argument("--cleanup-days", type=int, default=7, help="Clean up files older than N days")
    
    args = parser.parse_args()
    
    coordinator = VibeLayerSessionCoordinator(max_concurrent=args.max_concurrent)
    
    if args.cleanup:
        result = coordinator.cleanup_old_sessions(args.cleanup_days)
        print(json.dumps(result, indent=2))
        return
    
    if args.monitor:
        result = coordinator.monitor_sessions(args.monitor_timeout)
        print(json.dumps(result, indent=2, default=str))
        return
    
    if args.coordinate:
        result = coordinator.coordinate_parallel_development(args.stories_dir)
        print(json.dumps(result, indent=2))
        return
    
    # Default: show discovery results
    stories = coordinator.discover_stories(args.stories_dir)
    ready_stories = coordinator.get_ready_stories(stories)
    
    print(f"\n📚 Story Discovery Results:")
    print(f"Total stories found: {len(stories)}")
    print(f"Stories ready for development: {len(ready_stories)}")
    
    if ready_stories:
        print("\n🚀 Ready stories:")
        for story in ready_stories[:10]:  # Show first 10
            deps = ", ".join(story["dependencies"]) if story["dependencies"] else "none"
            print(f"  - {story['story_id']} (priority: {story['priority']}, deps: {deps})")

if __name__ == "__main__":
    main()