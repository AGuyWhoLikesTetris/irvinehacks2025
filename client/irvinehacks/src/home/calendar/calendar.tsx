import {useOutletContext} from "react-router-dom";
import React, {ChangeEvent, useEffect, useState} from "react";

import "./calendar.css";
import {useAuth0} from "@auth0/auth0-react";

type WeekDay = Array<{ courseName: string, courseType: string, time: Array<number>, id: string }>;

const colorSet = ["#ff6c6c", "#ffc969", "#67aeff", "#7e67ff", "#d067ff", "#ff67d3", "#46d667"]

export default function Calendar() {
    const [offSet, setOffSet] = useState<number>(8);

    const [schedule, setSchedule] = useState<Array<WeekDay>>([[], [], [], [], []]);

    const {user} = useAuth0();
    const [friends, setFriends] = useState({});
    const [colors, setColors] = useState({});

    const [checked, setChecked] = useState({});

    // @ts-ignore
    const {setCurrPage} = useOutletContext();

    const getSchedule = () => {
        if (user != undefined) {
            const id: string = user.sub!;

            fetch(`http://localhost:8000/view/friends/day?id=${encodeURIComponent(id)}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
                .then((data) => {
                    setSchedule(data)
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

                    const ids: string[] = Object.keys(data.friends);

                    const newColors: { [id: string]: string } = {};

                    for (let i = 0; i < ids.length; i++) {
                        newColors[ids[i]] = colorSet[i];
                    }

                    setColors(newColors);
                })
        }
    }

    useEffect(() => {
        setCurrPage(0);

        update();
        getSchedule();
    }, [])

    const handleScroll = (e: React.WheelEvent<HTMLDivElement>) => {
        const {deltaY} = e;
        setOffSet(Math.min(Math.max(Math.floor(offSet + deltaY / 100), 6), 15));
    }

    const onCheck = (e: ChangeEvent<HTMLInputElement>, id: string) => {
        const newChecked = {...checked}
        // @ts-ignore
        newChecked[id] = e.target.checked;

        setChecked(newChecked);
    }

    return (
        <div className="grow">
            <div className="flex h-full p-16 px-32 gap-14">
                <div onWheel={e => handleScroll(e)} className="w-full h-full calendarParent justify-items-center">
                    <div className="flex items-center">Monday</div>
                    <div className="flex items-center">Tuesday</div>
                    <div className="flex items-center">Wednesday</div>
                    <div className="flex items-center">Thursday</div>
                    <div className="flex items-center">Friday</div>
                    <Monday offSet={offSet} classes={schedule[0]} checkedList={checked} colorID={colors}/>
                    <WeekDay offSet={offSet} classes={schedule[1]} checkedList={checked} colorID={colors}/>
                    <WeekDay offSet={offSet} classes={schedule[2]} checkedList={checked} colorID={colors}/>
                    <WeekDay offSet={offSet} classes={schedule[3]} checkedList={checked} colorID={colors}/>
                    <WeekDay offSet={offSet} classes={schedule[4]} checkedList={checked} colorID={colors}/>
                </div>
                <div>
                    <div className="text-4xl text-center tracking-tight">Friends</div>
                    <div className="flex flex-col mt-4">
                        {Object.keys(friends).map((key, i) => {
                            return (
                                <div key={i} className="flex gap-2">
                                    <input className="cursor-pointer" type="checkbox"
                                           onChange={(e) => onCheck(e, key)}/>
                                    {/*@ts-ignore*/}
                                    <div className="text-xl">{friends[key]}</div>
                                </div>
                            )
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
}

function Monday({offSet, classes, checkedList, colorID}: {
    offSet: number,
    classes: WeekDay,
    checkedList: { [id: string]: boolean },
    colorID: { [id: string]: string }
}) {
    return (
        <div className="grid grid-rows-7 w-full">
            {[...Array(7)].map((_, i) =>
                <div key={i}
                     className={`relative border-t ${i == 6 ? "border-b" : ''} border-gray-500 flex items-center justify-center`}>
                    <div className="absolute -top-2.5 -left-5 text-sm">{calculateTime(i, offSet)}</div>
                    {i == 6 &&
                        <div className="absolute -bottom-2.5 -left-5 text-sm">{calculateTime(i + 1, offSet)}</div>}
                    {classes.map((element, j) => {
                        if (checkedList[element.id] && findStartPosition(element.time[0], i, offSet)) {
                            return (
                                <div key={j}
                                     className="absolute top-0 pt-3 text-white rounded-xl w-2/3 text-center opacity-70"
                                     style={{
                                         height: `${(element.time[1] - element.time[0]) * 100}%`,
                                         backgroundColor: colorID[element.id]
                                     }}>
                                    <p>{element.courseName}</p>
                                    <p className="text-sm">{element.courseType}</p>
                                </div>)
                        }
                    })}
                </div>
            )}
        </div>
    );
}

function WeekDay({offSet, classes, checkedList, colorID}: {
    offSet: number,
    classes: WeekDay,
    checkedList: { [id: string]: boolean },
    colorID: { [id: string]: string }
}) {
    return (
        <div className="grid grid-rows-7 w-full">
            {[...Array(7)].map((_, i) =>
                <div key={i}
                     className={`relative border-t ${i == 6 ? "border-b" : ''} border-gray-500 flex items-center justify-center`}>
                    {classes.map((element, j) => {
                        if (checkedList[element.id] && findStartPosition(element.time[0], i, offSet)) {
                            return (
                                <div key={j}
                                     className="absolute top-0 pt-3 text-white rounded-xl w-2/3 text-center opacity-70"
                                     style={{
                                         height: `${(element.time[1] - element.time[0]) * 100}%`,
                                         backgroundColor: colorID[element.id]
                                     }}>
                                    <p>{element.courseName}</p>
                                    <p className="text-sm">{element.courseType}</p>
                                </div>)
                        }
                    })}
                </div>
            )}
        </div>
    );
}

function calculateTime(index: number, offSet: number) {
    const time = (index + offSet) % 12;
    return time == 0 ? 12 : time;
}

function findStartPosition(time: number, index: number, offSet: number) {
    return (index + offSet <= time && time < (index + 1) + offSet)
}