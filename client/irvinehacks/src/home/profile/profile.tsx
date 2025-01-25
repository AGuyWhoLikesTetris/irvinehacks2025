import "./profile.css";
import {ReactNode, useEffect} from "react";
import {useOutletContext} from "react-router-dom";

const profile = {
    name: "Jalen Lukumura",
    school: "University of Chinese Immigrants",
    degree: "B.S. French Film Studies",
    grade: "Super-Senior",
    classes: ["HUM 1B", "HUM H1BS", "ICS 32", "MATH 3A"]
};

export default function Profile() {
    // @ts-ignore
    const {setCurrPage} = useOutletContext();

    useEffect(() => {
        setCurrPage(1);
    }, [])

    return (
        <div className="profileParent grow items-center pt-6 px-20">
            <div className="profileDiv1">
                <div className="flex flex-col items-start ml-16 gap-4">
                    <p className="text-center text-6xl p-4 border-4 border-black">{profile.name}</p>
                    <p className="text-center text-2xl mt-10">{profile.school}</p>
                    <p className="text-center text-2xl">{profile.degree}</p>
                    <p className="text-center text-2xl">{profile.grade}</p>
                </div>
            </div>
            <div className="profileDiv2">
                <img className="w-2/3 m-auto bg-sky-800 p-1 rounded-xl" src="https://i.redd.it/te843tecdv031.jpg"
                     alt="icon"/>
            </div>
            <div className="profileDiv3 h-full">
                <div className="flex flex-col w-3/4 h-full m-auto">
                    <p className="text-4xl mt-16">Classes:</p>
                    <div className="grow flex items-center justify-between w-full m-auto">
                        {profile.classes.map((name) =>
                            <Card>{name}</Card>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

function Card({children}: { children: Readonly<ReactNode> }) {
    return (
        <div className="w-52 h-32 border-4 border-amber-400 rounded-xl">
            <p className="text-center mt-6">{children}</p>
        </div>
    )
}