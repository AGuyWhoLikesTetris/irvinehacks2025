import {Outlet} from "react-router-dom";

export default function Home() {
    return (
        <div className="w-full h-full flex flex-col justify-between">
            <Outlet />
            <div className="flex w-full h-16">
                <div className="w-1/2 text-center bg-sky-800">
                    <img className="w-10 h-full m-auto" src="/calendarIcon.svg" alt="profile"/>
                </div>
                <div className="w-1/2 text-center bg-sky-600">
                    <img className="w-10 h-full m-auto" src="/profileIcon.svg" alt="profile"/>
                </div>
            </div>
        </div>
    );
}