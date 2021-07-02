import React from "react";
import socketio from "socket.io-client";

const host =  process.env.NODE_ENV !== 'production' ? "http://localhost:5000" : process.env.REACT_APP_AWS_ADDRESS
export const socket = socketio.connect(host);
export const SocketContext = React.createContext();
