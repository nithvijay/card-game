import React from "react";
import socketio from "socket.io-client";

const host =  process.env.NODE_ENV !== 'production' ? "http://localhost" : process.env.REACT_APP_AWS_ADDRESS
export const socket = socketio.connect(`${host}:5000`);
export const SocketContext = React.createContext();
