import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import './index.css'
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Home from "./home";
import Profile from "./home/profile";
import Calendar from "./home/calendar";

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <BrowserRouter>
            <Routes>
                <Route path="/home" element={<Home/>}>
                    <Route index element={<Profile/>}/>
                    <Route path="profile" element={<Profile/>}/>
                    <Route path="calendar" element={<Calendar/>}/>
                </Route>
            </Routes>
        </BrowserRouter>
    </StrictMode>
)
