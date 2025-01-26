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

    useEffect(() => {
        setCurrPage(1);

        if (user != undefined) {
            const id: string = user.sub!;

            fetch(`http://localhost:8000/view/user?id=${encodeURIComponent(id)}`, {
                method: "GET"
            }).then(res => res.json())
                .then(data => {
                    console.log(data)
                    setProfile({
                        name: data.name,
                        degree: data.major,
                        grade: YEAR[data.grade - 1],
                        classes: data.courses
                    });
                });
        }
    }, [])

    return (
        <div className="profileParent grow items-center pt-6 px-20">
            <div className="profileDiv1">
                <div className="flex flex-col items-center ml-16 gap-4">
                    <b className="text-center text-6xl p-6 bg-sky-50 border-4 border-sky-800 rounded-xl">{profile.name}</b>
                    <p className="text-center text-2xl">{profile.degree}</p>
                    <p className="text-center text-2xl">{profile.grade}</p>
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
                    <b className="text-4xl mt-16">Classes:</b>
                    <div className="grow flex items-center justify-between w-full m-auto">
                        {profile.classes.map((name, i) =>
                            <Card key={i}>{name}</Card>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

function Card({children}: { children: Readonly<ReactNode> }) {
    return (
        <div className="w-52 h-32 bg-[#fefbf2] border-4 border-amber-400 rounded-xl">
            <p className="text-center mt-6">{children}</p>
        </div>
    )
}