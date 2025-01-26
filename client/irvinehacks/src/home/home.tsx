import {Link, Outlet } from "react-router-dom";
import {useState} from "react";
import {useAuth0} from "@auth0/auth0-react";

export default function Home() {
    const [currPage, setCurrPage] = useState(0);
    const {logout, isAuthenticated} = useAuth0();

    return (
        <div className="w-full h-full flex flex-col justify-between">
            <div className="flex justify-between w-full text-3xl pt-5 px-7">
                <div><b>Zot</b>Sync</div>
                {isAuthenticated && <div className="cursor-pointer hover:text-neutral-600" onClick={() => logout({logoutParams: {returnTo: window.location.origin}})}>Logout</div>}
            </div>
            <Outlet context={{setCurrPage: setCurrPage}}/>
            <div className="flex w-full h-16">
                <Link to="/home/calendar"
                      className={`grow text-center ${currPage == 0 ? "bg-sky-600 hover:bg-sky-500" : "bg-sky-800 hover:bg-sky-700"}`}>
                    <img className="w-10 h-full m-auto" src="/calendarIcon.svg" alt="profile"/>
                </Link>
                <Link to="/home/profile"
                      className={`grow text-center ${currPage == 1 ? "bg-sky-600 hover:bg-sky-500" : "bg-sky-800 hover:bg-sky-700"}`}>
                    <img className="w-10 h-full m-auto" src="/profileIcon.svg" alt="profile"/>
                </Link>
                <Link to="/home/friends"
                      className={`grow text-center ${currPage == 2 ? "bg-sky-600 hover:bg-sky-500" : "bg-sky-800 hover:bg-sky-700"}`}>
                    <img className="w-10 h-full m-auto" src="/profileIcon.svg" alt="profile"/>
                </Link>
            </div>
        </div>
    );
}