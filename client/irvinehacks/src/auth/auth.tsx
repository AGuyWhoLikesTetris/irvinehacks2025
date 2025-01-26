import {useAuth0} from "@auth0/auth0-react";
import {useEffect} from "react";

export default function Auth() {
    const {user} = useAuth0();

    useEffect(() => {
        if (user != undefined) {
            const id: string = user.sub!;

            fetch(`http://localhost:8000/check_user_exists?id=${encodeURIComponent(id)}`, {
                mode: 'no-cors',
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            })
                .then(res => {console.log(res)})
                // .then(data => {
                //     console.log(data.exists)
                // });
        }
    }, []);

    return (
        <>auth</>
    )
}