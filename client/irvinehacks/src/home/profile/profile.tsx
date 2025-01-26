import "./profile.css";
import {ReactNode, useEffect, useState} from "react";
import {Link, useOutletContext} from "react-router-dom";
import {useAuth0} from "@auth0/auth0-react";

// const profile = {
//     name: "Jalen Lukumura",
//     school: "University of Chinese Immigrants",
//     degree: "B.S. French Film Studies",
//     grade: "Super-Senior",
//     classes: ["HUM 1B", "HUM H1BS", "ICS 32", "MATH 3A"]
// };

const YEAR = ["First-Year", "Second-Year", "Third-Year", "Fourth-Year"];

export default function Profile() {
    // @ts-ignore
    const {setCurrPage} = useOutletContext();
    const {user} = useAuth0();

    const [profile, setProfile] = useState({name: '', degree: '', grade: '', classes: []});
    const [classCode, setClassCode] = useState('');

    const updateCourses = () => {
        if (user != undefined) {
            const id: string = user.sub!;

            fetch(`http://localhost:8000/view/user?id=${encodeURIComponent(id)}`, {
                method: "GET"
            }).then(res => res.json())
                .then(data => {
                    setProfile({
                        name: data.name,
                        degree: data.major,
                        grade: YEAR[data.grade - 1],
                        classes: data.courses
                    });
                });
        }
    }

    const addClass = () => {
        if (user != undefined) {
            const id: string = user.sub!;

            // @ts-ignore
            if (classCode.length == 5 && !isNaN(classCode)) {
                fetch("http://localhost:8000/add/courses", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        id: id,
                        section_codes: [classCode]
                    })
                }).then(res => res.json())
                    .then(data => {
                        setClassCode('');

                        updateCourses();

                        if (!data.ok)
                            window.alert("Invalid code!")
                    })
            } else {
                window.alert("Invalid course code!")
            }
        }
    }

    const removeClass = (code: number) => {
        if (user != undefined) {
            const id: string = user.sub!;

            fetch("http://localhost:8000/delete/courses", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id: id,
                    section_codes: [code]
                })
            }).then(res => res.json())
                .then(data => {
                    updateCourses();

                    if (!data.ok)
                        window.alert("Oops! Internal server error!")
                })
        }
    }

    useEffect(() => {
        setCurrPage(1);

        updateCourses();
    }, [])

    return (
        <div className="profileParent grow items-center pt-6 px-20">
            <div className="profileDiv1">
                <div className="flex flex-col items-center ml-16 gap-4">
                    <b className="text-center text-6xl p-6 bg-sky-50 border-4 border-sky-800 rounded-xl">{profile.name == '' ? "Loading..." : profile.name}</b>
                    <p className="text-center text-2xl">Major: {profile.degree == '' ? "Loading..." : profile.degree}</p>
                    <p className="text-center text-2xl">Grade: {profile.grade == '' ? "Loading..." : profile.grade}</p>
                    <Link to="/settings" className="flex gap-2 border-b-[1.5px]">
                        <button className="text-xl leading-8 cursor-pointer"><b>Edit Profile</b></button>
                        <img className="-mt-0.5" width="20" src="/editIcon.svg" alt=''/>
                    </Link>
                </div>
            </div>
            <div className="profileDiv2">
                <img className="w-2/3 m-auto bg-sky-800 p-1 rounded-xl" src="https://i.redd.it/te843tecdv031.jpg"
                     alt="icon"/>
            </div>
            <div className="profileDiv3 h-full">
                <div className="flex flex-col w-3/4 h-full m-auto">
                    <div className="flex justify-between mt-16">
                        <b className="text-4xl">Classes:</b>
                        <div className="flex gap-2">
                            <input value={classCode} onChange={e => setClassCode(e.target.value)}
                                   className="text-lg w-32 border-4 border-sky-700 focus:outline-sky-800 focus:shadow-sky-800 bg-white rounded-lg px-2"
                                   type="text" maxLength={5}/>
                            <button onClick={addClass}
                                    className="bg-sky-700 hover:bg-sky-800 text-white p-3 rounded-lg cursor-pointer">
                                Add Class
                            </button>
                        </div>
                    </div>
                    <div className="grow flex items-center justify-around w-full m-auto gap-1">
                        {profile.classes.map((name: {
                                sectionCode: number,
                                courseName: string,
                                courseType: string
                            }, i) =>
                                <Card code={name.sectionCode} removeClass={removeClass}
                                      key={i}>{name.courseName}<br/>{name.courseType}</Card>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

function Card({code, removeClass, children}: {
    code: number,
    removeClass: (code: number) => void,
    children: Readonly<ReactNode>
}) {
    return (
        <div className="relative w-52 h-32 bg-[#fefbf2] border-4 border-amber-400 rounded-xl">
            <p className="text-center mt-6">{children}</p>
            <button onClick={() => removeClass(code)}
                    className="absolute -top-2 -right-2 w-6 h-6 bg-red-400 rounded-full text-center text-white cursor-pointer z-10">
                <b>–</b></button>
        </div>
    )
}