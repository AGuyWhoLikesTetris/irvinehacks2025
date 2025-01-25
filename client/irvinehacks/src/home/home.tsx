import {Outlet} from "react-router-dom";
//import {createContext, useState} from "react";

//export const HomeContext = createContext<boolean>(true);

export default function Home() {
    //const [onProfile, setOnProfile] = useState(true);

    return (
        <div className="w-full h-full flex flex-col justify-between">
            <Outlet/>
            <div className="flex w-full h-16">
                <div className="w-1/2 text-center bg-sky-800 hover:bg-sky-700">
                    <img className="w-10 h-full m-auto" src="/calendarIcon.svg" alt="profile"/>
                </div>
                <div className="w-1/2 text-center bg-sky-600 hover:bg-sky-500">
                    <img className="w-10 h-full m-auto" src="/profileIcon.svg" alt="profile"/>
                </div>
            </div>
        </div>
    );
}