import {useOutletContext} from "react-router-dom";
import {useEffect} from "react";

const friends = ["Leyiluuu", "Tetris Slut", "Bean", "Makani Pepperoni", "Hodak Nak"];
const friendRequests = ["LeBron", "Cousin Luigi", "Oswald", "Biden"];

export default function Friends() {
    // @ts-ignore
    const {setCurrPage} = useOutletContext();

    useEffect(() => {
        setCurrPage(2);
    }, [])

    return (
        <div className="grow p-28 px-44">
            <div className="w-full flex justify-around">
                <div className="w-1/3 flex flex-col gap-5">
                    <div className="text-4xl mb-6 tracking-tight flex justify-between">
                        <b>Friends</b>
                        <div className="text-white text-2xl border-3 border-red-400 bg-red-400 rounded-full w-10 h-10 text-center leading-9">{friends.length}</div>
                    </div>
                    {friends.map((name, _) =>
                        <div className="border-3 border-sky-800 rounded-lg text-2xl p-5">{name}</div>
                    )}
                </div>
                <div className="w-1/3 flex flex-col gap-5">
                    <div className="text-4xl mb-6 tracking-tight flex justify-between">
                        <b>Friend Requests</b>
                        <div className="text-white text-2xl border-3 border-red-400 bg-red-400 rounded-full w-10 h-10 text-center leading-9">{friendRequests.length}</div>
                    </div>
                    {friendRequests.map((name, _) =>
                        <div className="flex justify-between items-center border-3 border-amber-400 rounded-lg p-5">
                            <div className="text-2xl ">{name}</div>
                            <div className="flex gap-6">
                                <button className="text-white border rounded-lg p-2 py-1 bg-[#28a745] hover:bg-[#1f8036]">Accept</button>
                                <button className="text-white border rounded-lg p-2 py-1 bg-red-400 hover:bg-[#d65052]">Booooo</button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}