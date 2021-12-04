import axios from 'axios'


let auth = "Bearer " + sessionStorage.getItem("access_token")
export default axios.create({
    baseURL: 'https://scaler-assignment-api.herokuapp.com/',
    headers: {
        Secret: 'wgrapspo59RJeF2aiNDG8qG',
        Authorization: auth
    },
});