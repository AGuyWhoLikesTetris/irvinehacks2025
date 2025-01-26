import {useAuth0} from "@auth0/auth0-react";
import {useEffect} from "react";
import {useNavigate} from "react-router-dom";

export default function Auth() {
    const {user} = useAuth0();
    const navigate = useNavigate();

    useEffect(() => {
        if (user != undefined) {
            const id: string = user.sub!;

            fetch(`http://localhost:8000/check_user_exists?id=${encodeURIComponent(id)}`, {
                method: "GET"
            })
                .then(res => res.json())
                .then(data => {
                    if (data.exists) {
                        navigate("/home");
                    } else {
                        navigate("/signup");
                    }
                });
        }
    }, []);

    return (
        <>auth</>
    )
}