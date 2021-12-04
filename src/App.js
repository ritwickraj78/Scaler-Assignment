import './App.css';
import {Route, Routes} from "react-router-dom";
import SignIn from "./Pages/LoginPage";
import HomePage from "./Pages/HomePage";

function App() {
    return (
        <div className="App">
            <Routes>
                <Route
                    exact
                    path='/'
                    element={<SignIn/>}
                />
                <Route
                    exact
                    path='/home'
                    element={<HomePage/>}
                />
            </Routes>
        </div>
    );
}

export default App;
