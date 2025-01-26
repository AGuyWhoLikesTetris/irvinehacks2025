import {useAuth0} from "@auth0/auth0-react";
import {useEffect} from "react";
import {useNavigate} from "react-router-dom";

export default function Login() {
    const {loginWithRedirect, isAuthenticated} = useAuth0();
    const navigate = useNavigate();

    useEffect(() => {
        navigate("/login");
    }, [])

    if (!isAuthenticated) {
        return (
            <div className="w-full h-full bg-slate-300">
                <div className="w-full text-3xl pt-5 pl-7"><b>Zot</b>Sync</div>

                <div className="flex flex-col items-center justify-around min-w-72 w-1/4 h-3/5 m-auto mt-28 border-4 border-sky-700 bg-sky-50 rounded-xl">
                    <img width="280" src="/zotsync.png" alt="logo"/>
                    <button className="w-2/3 h-14 bg-sky-700 hover:bg-sky-800 text-white text-xl tracking-wider rounded-sm cursor-pointer"
                        onClick={() => loginWithRedirect({authorizationParams: {redirect_uri: 'http://localhost:5173/auth'}})}>Log
                        In
                    </button>
                    <div className="mx-14 text-center">Log in to view your schedule and connect with friends!</div>
                </div>
            </div>
        )
    }
}