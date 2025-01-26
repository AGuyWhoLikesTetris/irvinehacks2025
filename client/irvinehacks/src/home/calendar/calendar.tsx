import {useOutletContext} from "react-router-dom";
import React, {useEffect, useState} from "react";

import "./calendar.css";

export default function Calendar() {
    const [offSet, setOffSet] = useState<number>(8);

    // @ts-ignore
    const {setCurrPage} = useOutletContext();

    useEffect(() => {
        setCurrPage(0);
    }, [])

    const handleScroll = (e: React.WheelEvent<HTMLDivElement>) => {
        const { deltaY } = e;
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
                    <Monday offSet={offSet}/>
                    <WeekDay/>
                    <WeekDay/>
                    <WeekDay/>
                    <WeekDay/>
                </div>
            </div>
        </div>
    );
}

function Monday({offSet}: {offSet: number}) {
    return (
        <div className="grid grid-rows-7 w-full">
            {[...Array(7)].map((_, i) =>
                <div key={i} className={`relative border-t ${i == 6 ? "border-b" : ''} border-gray-500 flex items-center justify-center`}>
                    <div className="absolute -top-2.5 -left-5 text-sm">{calculateTime(i, offSet)}</div>
                    {i == 6 ? <div className="absolute -bottom-2.5 -left-5 text-sm">{calculateTime(i + 1, offSet)}</div> : <></>}
                </div>
            )}
        </div>
    );
}

function WeekDay() {
    return (
        <div className="grid grid-rows-7 w-full">
            {[...Array(7)].map((_, i) =>
                <div key={i} className={`border-t ${i == 6 ? "border-b" : ''} border-gray-500 flex items-center justify-center`}></div>
            )}
        </div>
    );
}

function calculateTime(index: number, offSet: number) {
    const time = (index + offSet) % 12;
    return time == 0 ? 12 : time;
}