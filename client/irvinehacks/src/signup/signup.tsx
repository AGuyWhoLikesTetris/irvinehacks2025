import {FormEvent, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {useNavigate} from "react-router-dom";


export default function Signup() {
    const [name, setName] = useState("");
    const [major, setMajor] = useState("");
    const [year, setYear] = useState(1);
    const {user} = useAuth0();
    const navigate = useNavigate();

    const submitForm = (formData: FormEvent) => {
        formData.preventDefault();

        if (user != undefined) {
            const id: string = user.sub!;

            fetch("http://localhost:8000/add/user", {
                method: "POST",
                body: JSON.stringify({
                    id: id,
                    name: name,
                    major: major,
                    grade: year
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(res => res.json())
                .then(data => {
                    if (data.ok) {
                        navigate("/home");
                    }
                })
        }
    }


    return (
        <div className="w-full h-full bg-zinc-300">
            <div className="w-full text-3xl pt-5 pl-7"><b>Zot</b>Sync</div>

            <div
                className="flex flex-col min-w-72 w-1/3 h-4/5 m-auto mt-14 border-4 border-sky-700 bg-sky-50 rounded-xl p-10 text-2xl">
                <div className="text-3xl mb-5 text-center">Signup</div>
                <form className="flex flex-col gap-3" onSubmit={submitForm}>
                    <label htmlFor="name">Name:</label>
                    <input id="name"
                           className="w-full border-3 border-sky-700 focus:outline-sky-800 bg-white rounded-lg px-2"
                           type="text"
                           value={name}
                           onChange={(e) => setName(e.target.value)}
                    />
                    <br/>
                    <label htmlFor="major">Major:</label>
                    <input id="major"
                           className="w-full border-3 border-sky-700 focus:outline-sky-800 bg-white rounded-lg px-2"
                           type="text"
                           value={major}
                           onChange={(e) => setMajor(e.target.value)}
                    />
                    <br/>
                    <div>Grade:</div>
                    <div>
                        <input id="first" type="radio" name="grade" value="1st-year" onClick={() => setYear(1)} />
                        <label className="ml-4" htmlFor="first">1st-year</label>
                    </div>
                    <div>
                        <input id="second" type="radio" name="grade" value="2nd-year" onClick={() => setYear(2)}/>
                        <label className="ml-4" htmlFor="second">2nd-year</label>
                    </div>
                    <div>
                        <input id="third" type="radio" name="grade" value="3rd-year" onClick={() => setYear(3)}/>
                        <label className="ml-4" htmlFor="third">3rd-year</label>
                    </div>
                    <div>
                        <input id="fourth" type="radio" name="grade" value="4th-year" onClick={() => setYear(4)}/>
                        <label className="ml-4" htmlFor="fourth">4th-year</label>
                    </div>
                    <input
                        type="submit"
                        className="p-2 py-1 rounded-sm cursor-pointer bg-[#28a745] hover:bg-[#1f8036] text-white mt-10"
                        value="Signup"
                    />
                </form>
            </div>
        </div>
    );
}