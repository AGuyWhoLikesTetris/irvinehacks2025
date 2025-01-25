import {Link, Outlet} from "react-router-dom";
import {useState} from "react";

export default function Home() {
    const [onProfile, setOnProfile] = useState(true);

    return (
        <div className="w-full h-full flex flex-col justify-between">
            <Outlet context={{setOnProfile: setOnProfile}}/>
            <div className="flex w-full h-16">
                <Link to="/home/calendar"
                      className={`w-1/2 text-center ${onProfile ? "bg-sky-800 hover:bg-sky-700" : "bg-sky-600 hover:bg-sky-500"}`}>
                    <img className="w-10 h-full m-auto" src="/calendarIcon.svg" alt="profile"/>
                </Link>
                <Link to="/home/profile"
                      className={`w-1/2 text-center ${onProfile ? "bg-sky-600 hover:bg-sky-500" : "bg-sky-800 hover:bg-sky-700"}`}>
                    <img className="w-10 h-full m-auto" src="/profileIcon.svg" alt="profile"/>
                </Link>
            </div>
        </div>
    );
}