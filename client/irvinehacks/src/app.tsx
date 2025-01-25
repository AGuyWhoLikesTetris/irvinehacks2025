import {BrowserRouter, Route, Routes} from "react-router-dom";
import Home from "./home";
import Profile from "./home/profile";
import Calendar from "./home/calendar";
import Friends from "./home/friends";


export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/home" element={<Home/>}>
                    <Route index element={<Profile/>}/>
                    <Route path="profile" element={<Profile/>}/>
                    <Route path="calendar" element={<Calendar/>}/>
                    <Route path="friends" element={<Friends/>}/>
                </Route>
            </Routes>
        </BrowserRouter>
    )
}