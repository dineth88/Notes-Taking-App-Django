import axios from "axios"
import {ACCESS_TOKEN} from "./constants"

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
})

api.interceptors.request.use(
    (config) =>{
        //localStorage is a web storage object that allows
        // JavaScript sites and apps to keep key-value 
        //pairs in a web browser with no expiration date
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = 'Bearer ${token}'
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default api