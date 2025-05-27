import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './components/Landing'
import Home from "./components/Home"
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';

function App() {
  return (
    <>
    <ToastContainer position="top-right" autoClose={3000} />
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/home" element={<Home />}/>
      </Routes>
    </Router>
    </>
  );
}

export default App;
