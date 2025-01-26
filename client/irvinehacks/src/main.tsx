import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import './index.css'
import App from "./app.tsx";
import {Auth0Provider} from "@auth0/auth0-react";

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <Auth0Provider domain='dev-zndrm7d432htvwph.us.auth0.com' clientId='hSTjNOmQgWoZXBMr9H8Zpt6AMom838vE' authorizationParams={{redirect_uri: window.location.origin }}>
            <App/>
        </Auth0Provider>
    </StrictMode>
)
