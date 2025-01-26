import {BrowserRouter, Navigate, Route, Routes} from "react-router-dom";
import Home from "./home";
import Profile from "./home/profile";
import Calendar from "./home/calendar";
import Friends from "./home/friends";

import Login from "./login";
import {useAuth0} from "@auth0/auth0-react";
import Settings from "./home/settings";

export default function App() {
    const { isAuthenticated, isLoading } = useAuth0();

    if (isLoading) {
        return <div>Loading...</div>
    }

    return (
        <BrowserRouter>
            {isAuthenticated ? (
                <Routes>
                    <Route path="/" element={<Navigate to="/home"/>}/>
                    <Route path="/home" element={<Home/>}>
                        <Route index element={<Profile/>}/>
                        <Route path="profile" element={<Profile/>}/>
                        <Route path="calendar" element={<Calendar/>}/>
                        <Route path="friends" element={<Friends/>}/>
                    </Route>
                    <Route path="settings" element={<Settings/>}/>
                </Routes>
            ) : (
                <Login/>
            )}
        </BrowserRouter>
    )
}