import {useOutletContext} from "react-router-dom";
import {useEffect} from "react";

export default function Calendar() {
    // @ts-ignore
    const {setOnProfile} = useOutletContext();

    useEffect(() => {
        setOnProfile(false);
    }, [])

    return (
        <>calendar</>
    );
}