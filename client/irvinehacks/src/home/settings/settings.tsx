import {Link} from "react-router-dom";

export default function Settings() {



    return (
        <div className="w-full h-full bg-zinc-300">
            <div className="w-full text-3xl pt-5 pl-7"><b>Zot</b>Sync</div>

            <div
                className="flex flex-col min-w-72 w-1/3 h-4/5 m-auto mt-14 border-4 border-sky-700 bg-sky-50 rounded-xl p-10 text-2xl">
                <div className="text-3xl mb-5">Settings</div>
                <form className="flex flex-col gap-3 grow">
                    <label htmlFor="name">Name:</label>
                    <input id="name"
                           className="w-full border-3 border-sky-700 focus:outline-sky-800 bg-white rounded-lg px-2"
                           type="text"/>
                    <br/>
                    <label htmlFor="major">Major:</label>
                    <input id="major"
                           className="w-full border-3 border-sky-700 focus:outline-sky-800 bg-white rounded-lg px-2"
                           type="text"/>
                    <br/>
                    <div>Grade:</div>
                    <div>
                        <input id="first" type="radio" name="grade" value="1st-year"/>
                        <label className="ml-4" htmlFor="first">1st-year</label>
                    </div>
                    <div>
                        <input id="second" type="radio" name="grade" value="2nd-year"/>
                        <label className="ml-4" htmlFor="second">2nd-year</label>
                    </div>
                    <div>
                        <input id="third" type="radio" name="grade" value="3rd-year"/>
                        <label className="ml-4" htmlFor="third">3rd-year</label>
                    </div>
                    <div>
                        <input id="fourth" type="radio" name="grade" value="4th-year"/>
                        <label className="ml-4" htmlFor="fourth">4th-year</label>
                    </div>
                    <div className="flex justify-between mt-10">
                        <Link to="/home/profile">
                            <button
                                className="p-2 py-1 rounded-sm cursor-pointer bg-red-400 hover:bg-[#d65052] text-white">Cancel
                            </button>
                        </Link>
                        <button
                            className="p-2 py-1 rounded-sm cursor-pointer bg-[#28a745] hover:bg-[#1f8036] text-white">Save
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}