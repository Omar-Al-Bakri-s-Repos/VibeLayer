import { generateId } from '@vibelayer/shared';

export default function HomePage() {
  const sessionId = generateId();

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            VibeLayer Control Panel
          </h1>
          <p className="text-xl text-purple-200">
            AI-powered visual effects and interaction system
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
            <h2 className="text-2xl font-semibold text-white mb-3">
              AI Agents
            </h2>
            <p className="text-purple-200 mb-4">
              Manage and configure AI agents for real-time interactions
            </p>
            <div className="text-sm text-purple-300">
              Session ID: {sessionId}
            </div>
          </div>
          
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
            <h2 className="text-2xl font-semibold text-white mb-3">
              Visual Overlays
            </h2>
            <p className="text-purple-200 mb-4">
              Create and customize real-time visual effects and overlays
            </p>
            <button className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors">
              Launch Editor
            </button>
          </div>
          
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
            <h2 className="text-2xl font-semibold text-white mb-3">
              Analytics
            </h2>
            <p className="text-purple-200 mb-4">
              Monitor system performance and user interactions
            </p>
            <div className="text-green-400 font-mono text-sm">
              Status: Online
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
