import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import NavBar from './components/navbar';
import Home from './pages/home';

function App() {
  return (
    <div className="App">
      <Router>
        {/* <NavBar/> */}
        <Routes>
          <Route exact path = "/" element={<Home/>}/>
        </Routes>

      </Router>
    </div>
  );
}

export default App;
