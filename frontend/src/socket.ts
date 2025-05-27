import { io } from "socket.io-client";

const apiUrl = process.env.REACT_APP_API_URL;
const port = process.env.REACT_APP_PORT;

const socket = io(`${apiUrl}:${port}`);

export default socket;