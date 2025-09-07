#!/usr/bin/env python3
"""
VibeLayer Parallel Agent Orchestrator
Spawns multiple Claude Code agents in Depot sandboxes for parallel story development.
"""
import os
import json
import subprocess
import hashlib
import time
import asyncio
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class ParallelAgentOrchestrator:
    def __init__(self, project_root: str = "/home/omar/Documents/VibeLayer"):
        self.project_root = Path(project_root)
        self.session_store = self.project_root / ".depot/sessions"
        self.session_store.mkdir(parents=True, exist_ok=True)
        self.depot_path = "/home/omar/.depot/bin/depot"
        
    def generate_session_id(self, story_id: str) -> str:
        """Generate session ID for story-based development"""
        timestamp = int(time.time())
        return f"vibelayer-{story_id.replace('.', '-')}-{timestamp}"
    
    def create_story_prompt(self, story_file: Path, story_id: str) -> str:
        """Create development prompt from story file"""
        story_content = story_file.read_text(encoding='utf-8')
        
        prompt = f"""You are a development agent working on Story {story_id} for VibeLayer.

STORY CONTENT:
{story_content}

INSTRUCTIONS:
1. Implement ALL unchecked tasks in the story
2. Follow the acceptance criteria exactly
3. Use the existing monorepo structure
4. Write clean, tested, production-ready code
5. Update the story file marking tasks as complete
6. Commit your changes with descriptive messages

Start by reading the story file and understanding what needs to be done.
Then implement each task systematically."""
        
        return prompt
    
    def spawn_agent(self, story_file: Path, story_id: str, wait: bool = False) -> Dict:
        """Spawn a single Claude agent for a story"""
        session_id = self.generate_session_id(story_id)
        prompt = self.create_story_prompt(story_file, story_id)
        
        # Build depot claude command
        cmd = [
            self.depot_path, "claude",
            "--session-id", session_id,
            "--repository", "https://github.com/OmarA1-Bakri/VibeLayer",
            "--branch", "main",
            "-p",  # Print mode for automation
            prompt
        ]
        
        if wait:
            cmd.insert(2, "--wait")  # Add wait flag after 'claude'
        
        session_data = {
            "session_id": session_id,
            "story_id": story_id,
            "story_file": str(story_file),
            "started_at": datetime.now().isoformat(),
            "status": "starting"
        }
        
        try:
            print(f"🚀 Spawning agent for Story {story_id} (Session: {session_id})")
            
            # Start the process
            if wait:
                # Synchronous execution with wait
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=3600,  # 1 hour timeout for wait mode
                    env={**os.environ, "PATH": f"{os.path.dirname(self.depot_path)}:{os.environ.get('PATH', '')}"}
                )
                
                session_data["status"] = "completed" if result.returncode == 0 else "failed"
                session_data["output"] = result.stdout
                session_data["error"] = result.stderr
                
                # Extract session URL from output
                for line in result.stdout.split('\n'):
                    if 'Link:' in line:
                        session_data["session_url"] = line.split('Link:')[1].strip()
                        break
                
            else:
                # Asynchronous spawn without waiting
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env={**os.environ, "PATH": f"{os.path.dirname(self.depot_path)}:{os.environ.get('PATH', '')}"}
                )
                
                # Wait briefly for session to start
                time.sleep(3)
                
                # Get initial output
                try:
                    stdout, stderr = process.communicate(timeout=5)
                    session_data["output"] = stdout
                    session_data["error"] = stderr
                    session_data["status"] = "running"
                    
                    # Extract session URL
                    for line in stdout.split('\n'):
                        if 'Link:' in line:
                            session_data["session_url"] = line.split('Link:')[1].strip()
                            break
                            
                except subprocess.TimeoutExpired:
                    # Process is still running (expected for non-wait mode)
                    session_data["status"] = "running"
                    session_data["output"] = "Agent spawned and running in background"
            
            # Save session data
            session_file = self.session_store / f"{session_id}.json"
            session_file.write_text(json.dumps(session_data, indent=2))
            
            if session_data.get("session_url"):
                print(f"✅ Agent for Story {story_id} started: {session_data['session_url']}")
            else:
                print(f"✅ Agent for Story {story_id} started (Session: {session_id})")
                
        except Exception as e:
            session_data["status"] = "error"
            session_data["error"] = str(e)
            print(f"❌ Failed to spawn agent for Story {story_id}: {e}")
        
        return session_data
    
    def spawn_parallel_agents(self, story_files: List[Path], max_concurrent: int = 5) -> Dict:
        """Spawn multiple agents in parallel"""
        results = {
            "sessions": [],
            "successful": 0,
            "failed": 0,
            "total": len(story_files)
        }
        
        print(f"\n🎯 Spawning {len(story_files)} agents (max {max_concurrent} concurrent)")
        print("=" * 60)
        
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            # Submit all tasks
            future_to_story = {}
            for story_file in story_files:
                story_id = story_file.stem.replace('story_', '')
                future = executor.submit(self.spawn_agent, story_file, story_id, wait=False)
                future_to_story[future] = (story_file, story_id)
                time.sleep(2)  # Stagger spawns slightly
            
            # Collect results
            for future in as_completed(future_to_story):
                story_file, story_id = future_to_story[future]
                try:
                    session_data = future.result(timeout=60)
                    results["sessions"].append(session_data)
                    
                    if session_data["status"] in ["running", "completed"]:
                        results["successful"] += 1
                    else:
                        results["failed"] += 1
                        
                except Exception as e:
                    print(f"❌ Exception for Story {story_id}: {e}")
                    results["failed"] += 1
                    results["sessions"].append({
                        "story_id": story_id,
                        "status": "exception",
                        "error": str(e)
                    })
        
        print("\n" + "=" * 60)
        print(f"📊 Results: {results['successful']} successful, {results['failed']} failed")
        
        return results
    
    def monitor_sessions(self, session_ids: List[str] = None) -> Dict:
        """Monitor running sessions"""
        if session_ids is None:
            # Get all running sessions
            session_ids = []
            for session_file in self.session_store.glob("*.json"):
                try:
                    data = json.loads(session_file.read_text())
                    if data.get("status") == "running":
                        session_ids.append(data["session_id"])
                except:
                    continue
        
        print(f"\n📊 Monitoring {len(session_ids)} sessions...")
        
        statuses = {}
        for session_id in session_ids:
            # Check depot session status
            cmd = [self.depot_path, "claude", "--resume", session_id, "--wait"]
            
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    env={**os.environ, "PATH": f"{os.path.dirname(self.depot_path)}:{os.environ.get('PATH', '')}"}
                )
                
                statuses[session_id] = {
                    "status": "completed" if result.returncode == 0 else "running",
                    "output": result.stdout[:500]  # First 500 chars
                }
                
            except subprocess.TimeoutExpired:
                statuses[session_id] = {"status": "running"}
            except Exception as e:
                statuses[session_id] = {"status": "error", "error": str(e)}
        
        return statuses
    
    def list_sessions(self) -> List[Dict]:
        """List all sessions"""
        sessions = []
        
        # Get depot sessions list
        cmd = [self.depot_path, "claude", "list-sessions", "--output", "json"]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                env={**os.environ, "PATH": f"{os.path.dirname(self.depot_path)}:{os.environ.get('PATH', '')}"}
            )
            
            if result.returncode == 0 and result.stdout:
                depot_sessions = json.loads(result.stdout)
                sessions.extend(depot_sessions)
                
        except Exception as e:
            print(f"Warning: Could not get depot sessions: {e}")
        
        # Also check local session files
        for session_file in self.session_store.glob("*.json"):
            try:
                data = json.loads(session_file.read_text())
                sessions.append({
                    "session_id": data.get("session_id"),
                    "story_id": data.get("story_id"),
                    "status": data.get("status"),
                    "started_at": data.get("started_at"),
                    "url": data.get("session_url")
                })
            except:
                continue
        
        return sessions


def main():
    """CLI interface for parallel agent orchestrator"""
    parser = argparse.ArgumentParser(description="Orchestrate parallel Claude agents for story development")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Spawn command
    spawn_parser = subparsers.add_parser("spawn", help="Spawn agents for stories")
    spawn_parser.add_argument("--stories", nargs="+", help="Story file paths")
    spawn_parser.add_argument("--all", action="store_true", help="Spawn for all stories in docs/stories/")
    spawn_parser.add_argument("--max-concurrent", type=int, default=5, help="Max concurrent agents")
    spawn_parser.add_argument("--epic", help="Spawn all stories for specific epic (e.g., 1)")
    
    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Monitor running sessions")
    monitor_parser.add_argument("--sessions", nargs="+", help="Specific session IDs to monitor")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all sessions")
    
    args = parser.parse_args()
    
    orchestrator = ParallelAgentOrchestrator()
    
    if args.command == "spawn":
        story_files = []
        
        if args.all:
            # Get all story files
            story_dir = orchestrator.project_root / "docs/stories"
            story_files = list(story_dir.glob("*.md"))
            
        elif args.epic:
            # Get all stories for specific epic
            story_dir = orchestrator.project_root / "docs/stories"
            story_files = list(story_dir.glob(f"{args.epic}.*.md"))
            
        elif args.stories:
            # Use specified story files
            story_files = [Path(s) for s in args.stories]
        
        else:
            print("Error: Specify --stories, --all, or --epic")
            return
        
        # Filter out non-existent files
        story_files = [f for f in story_files if f.exists()]
        
        if not story_files:
            print("No story files found")
            return
        
        print(f"Found {len(story_files)} story files:")
        for f in story_files:
            print(f"  - {f.name}")
        
        # Spawn agents
        results = orchestrator.spawn_parallel_agents(story_files, args.max_concurrent)
        
        # Save results
        results_file = orchestrator.project_root / ".depot/orchestration-results.json"
        results_file.write_text(json.dumps(results, indent=2))
        
        print(f"\n✅ Results saved to {results_file}")
        
    elif args.command == "monitor":
        statuses = orchestrator.monitor_sessions(args.sessions)
        print(json.dumps(statuses, indent=2))
        
    elif args.command == "list":
        sessions = orchestrator.list_sessions()
        
        print("\n📋 All Sessions:")
        print("=" * 80)
        
        for session in sessions:
            status_emoji = {
                "running": "🔄",
                "completed": "✅",
                "failed": "❌",
                "error": "⚠️"
            }.get(session.get("status", ""), "❓")
            
            print(f"{status_emoji} {session.get('session_id', 'Unknown')}")
            print(f"   Story: {session.get('story_id', 'N/A')}")
            print(f"   Status: {session.get('status', 'Unknown')}")
            if session.get("url"):
                print(f"   URL: {session['url']}")
            print()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()