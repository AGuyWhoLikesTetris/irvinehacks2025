import {useOutletContext} from "react-router-dom";
import React, {useEffect, useState} from "react";

import "./calendar.css";

const courses = [
    {
        courseName: "MATH 3A",
        courseType: "Lec",
        days: "MWF",
        time: [
            {
                hour: 14,
                minute: 0,
            },
            {
                hour: 14,
                minute: 50,
            }
        ]
    }
]

type WeekDay = Array<{ courseName: string, courseType: string, time: Array<number> }>;

export default function Calendar() {
    const [offSet, setOffSet] = useState<number>(8);

    const [mondays, setMondays] = useState<WeekDay>([]);
    const [tuesdays, setTuesdays] = useState<WeekDay>([]);
    const [wednesdays, setWednesdays] = useState<WeekDay>([]);
    const [thursdays, setThursdays] = useState<WeekDay>([]);
    const [fridays, setFridays] = useState<WeekDay>([]);

    // @ts-ignore
    const {setCurrPage} = useOutletContext();

    useEffect(() => {
        setCurrPage(0);

        setMondays([
            {
                courseName: "MATH 3A",
                courseType: "Lec",
                time: [14, 14.83]
            },
            {
                courseName: "MATH 2D",
                courseType: "Lec",
                time: [16, 17.83]
            }
        ]);

        setThursdays([
            {
                courseName: "HUM 1A",
                courseType: "Lec",
                time: [11, 11.83]
            },
            {
                courseName: "HUM 1AS",
                courseType: "Lec",
                time: [16, 17.83]
            }
        ])
    }, [])

    const handleScroll = (e: React.WheelEvent<HTMLDivElement>) => {
        const {deltaY} = e;
        setOffSet(Math.min(Math.max(Math.floor(offSet + deltaY / 100), 6), 15));
    }

    return (
        <div className="grow">
            <div className="w-full h-full p-16 px-44">
                <div onWheel={e => handleScroll(e)} className="w-full h-full calendarParent justify-items-center">
                    <div className="flex items-center">Monday</div>
                    <div className="flex items-center">Tuesday</div>
                    <div className="flex items-center">Wednesday</div>
                    <div className="flex items-center">Thursday</div>
                    <div className="flex items-center">Friday</div>
                    <Monday offSet={offSet} schedule={mondays}/>
                    <WeekDay offSet={offSet} schedule={tuesdays}/>
                    <WeekDay offSet={offSet} schedule={wednesdays}/>
                    <WeekDay offSet={offSet} schedule={thursdays}/>
                    <WeekDay offSet={offSet} schedule={fridays}/>
                </div>
            </div>
        </div>
    );
}

function Monday({offSet, schedule}: { offSet: number, schedule: WeekDay }) {
    return (
        <div className="grid grid-rows-7 w-full">
            {[...Array(7)].map((_, i) =>
                <div key={i}
                     className={`relative border-t ${i == 6 ? "border-b" : ''} border-gray-500 flex items-center justify-center`}>
                    <div className="absolute -top-2.5 -left-5 text-sm">{calculateTime(i, offSet)}</div>
                    {i == 6 &&
                        <div className="absolute -bottom-2.5 -left-5 text-sm">{calculateTime(i + 1, offSet)}</div>}
                    {schedule.map((element) => {
                        if (findStartPosition(element.time[0], i, offSet)) {
                            return (
                                <div className="absolute top-0 pt-5 text-white rounded-xl w-2/3 text-center bg-red-400"
                                     style={{height: `${(element.time[1] - element.time[0]) * 100}%`}}>{element.courseName}</div>)
                        }
                    })}
                </div>
            )}
        </div>
    );
}

function WeekDay({offSet, schedule}: { offSet: number, schedule: WeekDay }) {
    return (
        <div className="grid grid-rows-7 w-full">
            {[...Array(7)].map((_, i) =>
                <div key={i}
                     className={`relative border-t ${i == 6 ? "border-b" : ''} border-gray-500 flex items-center justify-center`}>
                    {schedule.map((element) => {
                        if (findStartPosition(element.time[0], i, offSet)) {
                            return (
                                <div className="absolute top-0 pt-5 text-white rounded-xl w-2/3 text-center bg-red-400"
                                     style={{height: `${(element.time[1] - element.time[0]) * 100}%`}}>{element.courseName}</div>)
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