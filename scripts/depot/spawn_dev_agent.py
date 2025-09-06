#!/usr/bin/env python3
"""
VibeLayer Development Agent Spawner
Spawns BMAD development agents in Depot sandboxes for individual stories.
"""
import os
import json
import subprocess
import hashlib
import time
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime

class VibeLayerDevAgentSpawner:
    def __init__(self, project_root: str = "/home/omar/Documents/VibeLayer"):
        self.project_root = Path(project_root)
        self.session_store = self.project_root / ".depot/sessions"
        self.session_store.mkdir(parents=True, exist_ok=True)
        
    def generate_session_id(self, story_id: str, story_hash: str) -> str:
        """Generate deterministic session ID for story-based development"""
        timestamp = int(time.time())
        return f"vibelayer-dev-{story_id}-{story_hash[:8]}-{timestamp}"
    
    def get_story_hash(self, story_content: str) -> str:
        """Generate hash of story content for change detection"""
        return hashlib.sha256(story_content.encode()).hexdigest()
    
    def spawn_development_agent(self, story_file_path: str, story_id: str = None) -> Dict:
        """
        Spawn a development agent in Depot sandbox for a specific story
        
        Args:
            story_file_path: Path to the story file containing development context
            story_id: Optional story identifier (extracted from filename if not provided)
            
        Returns:
            Dict containing session information and monitoring details
        """
        story_path = Path(story_file_path)
        
        if not story_path.exists():
            raise FileNotFoundError(f"Story file not found: {story_file_path}")
        
        # Extract story ID from filename if not provided
        if not story_id:
            story_id = story_path.stem.replace('story_', '').replace('.md', '')
        
        # Read story content
        story_content = story_path.read_text(encoding='utf-8')
        story_hash = self.get_story_hash(story_content)
        
        # Generate session ID
        session_id = self.generate_session_id(story_id, story_hash)
        session_file = self.session_store / f"{session_id}.json"
        
        # Check for existing session with same story hash
        if session_file.exists():
            existing = json.loads(session_file.read_text())
            if existing.get("story_hash") == story_hash and existing.get("status") in ["running", "completed"]:
                print(f"Existing session found for story {story_id}: {existing.get('session_url', session_id)}")
                return existing
        
        # Create development prompt for the agent
        dev_prompt = self._create_development_prompt(story_content, story_id)
        
        # Build Depot command for development agent
        cmd = [
            "depot", "claude",
            "--session-id", session_id,
            "--repository", "VibeLayer",
            "--branch", os.environ.get("GITHUB_REF_NAME", "main"),
            "--allowedTools", "Bash,GitHub,FileSystem",
            dev_prompt
        ]
        
        try:
            print(f"Spawning development agent for story: {story_id}")
            print(f"Session ID: {session_id}")
            
            # Execute Depot command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1800,  # 30 minutes timeout
                cwd=self.project_root,
                env={**os.environ, "PATH": f"/home/omar/.depot/bin:{os.environ.get('PATH', '')}"}
            )
            
            if result.returncode == 0:
                # Extract session URL from output
                session_url = None
                for line in result.stdout.split('\n'):
                    if 'depot.dev' in line and 'http' in line:
                        session_url = line.strip()
                        break
                
                # Save session state
                session_data = {
                    "session_id": session_id,
                    "session_url": session_url,
                    "story_id": story_id,
                    "story_file": str(story_file_path),
                    "story_hash": story_hash,
                    "status": "running",
                    "started_at": datetime.utcnow().isoformat(),
                    "agent_type": "development",
                    "command_output": result.stdout[:1000]  # First 1000 chars
                }
                
                session_file.write_text(json.dumps(session_data, indent=2))
                
                print(f"✅ Development agent spawned successfully")
                print(f"📊 Monitor at: {session_url}")
                
                return session_data
            else:
                error_msg = f"Failed to spawn development agent: {result.stderr}"
                print(f"❌ {error_msg}")
                raise RuntimeError(error_msg)
                
        except subprocess.TimeoutExpired:
            error_msg = f"Development agent spawn timed out for story: {story_id}"
            print(f"⏰ {error_msg}")
            raise RuntimeError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error spawning development agent: {str(e)}"
            print(f"💥 {error_msg}")
            raise RuntimeError(error_msg)
    
    def _create_development_prompt(self, story_content: str, story_id: str) -> str:
        """
        Create a focused development prompt for the agent based on the story
        The story contains all necessary context, architecture, and implementation details
        """
        return f"""You are a Development Agent working on VibeLayer story: {story_id}

STORY CONTEXT:
{story_content}

INSTRUCTIONS:
1. Read and understand the complete story context above
2. The story contains all necessary implementation details, architecture guidance, and context
3. Implement the feature/changes exactly as specified in the story
4. Follow VibeLayer's existing code conventions and patterns
5. Create/modify files as needed to complete the implementation
6. Test your implementation to ensure it works correctly
7. Commit your changes with a clear commit message referencing the story ID

IMPORTANT:
- You only have access to this story context - no other artifacts
- The story is self-contained with all necessary information
- Focus on implementing exactly what the story describes
- Use VibeLayer's existing TypeScript, React, Next.js patterns
- Follow the monorepo structure with proper package dependencies

Begin implementation of story {story_id}:"""
    
    def get_session_status(self, session_id: str) -> Dict:
        """Get current status of a development agent session"""
        session_file = self.session_store / f"{session_id}.json"
        
        if not session_file.exists():
            return {"error": f"Session {session_id} not found"}
        
        session_data = json.loads(session_file.read_text())
        
        # Try to get live status from Depot if possible
        try:
            # This would require Depot CLI status command - placeholder for now
            # In real implementation, use: depot session status {session_id}
            pass
        except Exception:
            pass
        
        return session_data
    
    def list_active_sessions(self) -> Dict:
        """List all active development agent sessions"""
        sessions = []
        
        for session_file in self.session_store.glob("*.json"):
            try:
                session_data = json.loads(session_file.read_text())
                if session_data.get("agent_type") == "development":
                    sessions.append({
                        "session_id": session_data["session_id"],
                        "story_id": session_data["story_id"],
                        "status": session_data["status"],
                        "started_at": session_data["started_at"],
                        "session_url": session_data.get("session_url")
                    })
            except (json.JSONDecodeError, KeyError):
                continue
        
        return {
            "active_sessions": sessions,
            "total_count": len(sessions)
        }

def main():
    """CLI interface for development agent spawner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Spawn BMAD development agents in Depot sandboxes")
    parser.add_argument("--story-file", required=True, help="Path to story file")
    parser.add_argument("--story-id", help="Story identifier (optional)")
    parser.add_argument("--list", action="store_true", help="List active sessions")
    parser.add_argument("--status", help="Get status of specific session")
    
    args = parser.parse_args()
    
    spawner = VibeLayerDevAgentSpawner()
    
    if args.list:
        sessions = spawner.list_active_sessions()
        print(json.dumps(sessions, indent=2))
        return
    
    if args.status:
        status = spawner.get_session_status(args.status)
        print(json.dumps(status, indent=2))
        return
    
    # Spawn development agent
    try:
        session_data = spawner.spawn_development_agent(args.story_file, args.story_id)
        print(json.dumps(session_data, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()