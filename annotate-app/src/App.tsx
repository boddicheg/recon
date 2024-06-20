import './index.css';
import HeaderComponent from './components/HeaderComponent';

function App() {

  return (
    <>
      <div>
      <HeaderComponent />
      <main className="p-4">
        <h2>Welcome to My App</h2>
        <p>This is a simple React app with a header component.</p>
      </main>
    </div>
    </>
  )
}

export default App
