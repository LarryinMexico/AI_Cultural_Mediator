import { useSocket } from './hooks/useSocket'
import { AudioCapture } from './components/AudioCapture'
import { TranscriptView } from './components/TranscriptView'
import { SidePanel } from './components/SidePanel'
import { StatusIndicator } from './components/StatusIndicator'
import { TextInputTest } from './components/TextInputTest'

function App() {
  useSocket(); // Initialize socket connection

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col md:flex-row">
      {/* Main Content */}
      <div className="flex-1 p-8 flex flex-col gap-6 max-w-4xl mx-auto w-full">
        <header className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">(Half)Local AI Cultural Mediator</h1>
          <StatusIndicator />
        </header>

        <section className="flex flex-col gap-4 flex-1">
          <AudioCapture />
          <TextInputTest />
          <TranscriptView />
        </section>
      </div>

      {/* Side Panel */}
      <SidePanel />
    </div>
  )
}

export default App
