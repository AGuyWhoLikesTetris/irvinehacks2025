import {useOutletContext} from "react-router-dom";
import {FormEvent, useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";

export default function Friends() {
    // @ts-ignore
    const {setCurrPage} = useOutletContext();

    const [searchTerm, setSearchTerm] = useState("");
    const [searchResult, setSearchResult] = useState<Array<{ id: string, name: string }>>([]);

    const [friends, setFriends] = useState({});
    const [friendRequests, setFriendRequests] = useState({});

    const {user} = useAuth0();

    const search = (formData: FormEvent) => {
        formData.preventDefault();

        fetch(`http://localhost:8000/search/users?keyword=${encodeURIComponent(searchTerm)}`, {
            method: "GET"
        }).then(response => response.json())
            .then((data) => {
                setSearchResult(data.users)
            })
    }

    const sendRequest = (friendID: string) => {
        if (user != undefined) {
            const id: string = user.sub!;

            fetch("http://localhost:8000/add/friend_request", {
                method: "POST",
                body: JSON.stringify({
                    id: id,
                    friend_id: friendID
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
                .then((data) => {
                    if (!data.ok) {
                        window.alert("Oops! Internal server error!");
                    }
                })
        }
    }

    const addFriend = (friendID: string) => {
        if (user != undefined) {
            const id: string = user.sub!;

            fetch("http://localhost:8000/add/friend", {
                method: "POST",
                body: JSON.stringify({
                    id: id,
                    friend_id: friendID
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
                .then((data) => {
                    if (!data.ok) {
                        window.alert("Oops! Internal server error!");
                    }

                    update();
                })
        }
    }

    const rejectFriend = (friendID: string) => {
        if (user != undefined) {
            const id: string = user.sub!;

            fetch("http://localhost:8000/delete/friend_request", {
                method: "POST",
                body: JSON.stringify({
                    id: id,
                    friend_id: friendID
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
                .then((data) => {
                    if (!data.ok) {
                        window.alert("Oops! Internal server error!");
                    }

                    update();
                })
        }
    }

    const update = () => {
        if (user != undefined) {
            const id: string = user.sub!;

            fetch(`http://localhost:8000/view/user?id=${encodeURIComponent(id)}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
                .then((data) => {
                    setFriends(data.friends);
                    setFriendRequests(data.friendReqs);
                })
        }
    }

    useEffect(() => {
        setCurrPage(2);
        update();
    }, [])

    return (
        <div className="grow p-16 px-44">
            <div className="w-full flex justify-around">
                <div className="w-1/4 flex flex-col gap-5">
                    <div className="text-4xl mb-6 tracking-tight flex justify-between">
                        <b>Friends</b>
                        <div
                            className="text-white text-2xl border-3 border-red-400 bg-red-400 rounded-full w-10 h-10 text-center leading-9">{Object.keys(friends).length}</div>
                    </div>
                    {Object.keys(friends).map((id, i) => (
                        <div key={i} // @ts-ignore
                             className="bg-sky-50 border-3 border-sky-800 rounded-lg text-2xl p-5">{friends[id]}</div>
                    ))}
                </div>
                <div className="w-1/4 flex flex-col gap-5">
                    <div className="text-4xl mb-6 tracking-tight flex justify-between">
                        <b>Friend Requests</b>
                        <div
                            className="text-white text-2xl border-3 border-red-400 bg-red-400 rounded-full w-10 h-10 text-center leading-9">{Object.keys(friendRequests).length}</div>
                    </div>
                    {Object.keys(friendRequests).map((id, i) =>
                        <div key={i}
                             className="flex justify-between items-center border-3 border-amber-400 rounded-lg p-5 bg-[#fefbf2]">
                            {/* @ts-ignore */}
                            <div className="text-2xl ">{friendRequests[id]}</div>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => addFriend(id)}
                                    className="text-white cursor-pointer border rounded-lg p-2 py-1 bg-[#28a745] hover:bg-[#1f8036]">Accept
                                </button>
                                <button
                                    onClick={() => rejectFriend(id)}
                                    className="text-white cursor-pointer border rounded-lg p-2 py-1 bg-red-400 hover:bg-[#d65052]">Reject
                                </button>
                            </div>
                        </div>
                    )}
                </div>
                <div className="w-1/4 flex flex-col gap-5">
                    <div className="text-4xl mb-6 tracking-tight">
                        <b>Search</b>
                    </div>
                    <form className="flex" onSubmit={search}>
                        <input placeholder="search"
                               value={searchTerm}
                               onChange={(e) => setSearchTerm(e.target.value)}
                               className="w-full text-2xl border-3 border-sky-700 focus:outline-sky-800 bg-white rounded-l-lg px-2 py-1"
                               type="text"/>
                        <input
                            className="bg-sky-700 hover:bg-sky-800 cursor-pointer text-white rounded-r-lg text-lg px-2"
                            type="submit" value="Search"/>
                    </form>
                    {searchResult.map((result, i) => (
                        <div key={i}
                             className="flex justify-between bg-sky-50 border-3 border-sky-800 rounded-lg text-2xl p-5">
                            <div>{result.name}</div>
                            <button onClick={() => sendRequest(result.id)}
                                    className="text-sm cursor-pointer bg-[#ffc107] hover:bg-[#d6a207] px-2 rounded-lg">Send
                                Request
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}