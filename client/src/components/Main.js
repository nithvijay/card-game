import { useState, useContext, useCallback, useEffect } from "react";
import { SocketContext } from "../context/socket";

import MessageBox from "./MessageBox";
import PlayingArea from "./PlayingArea";

const Main = () => {
  const socket = useContext(SocketContext);
  const [username, setUsername] = useState("");
  const [room, setRoom] = useState("");
  const [enteredRoom, setEnteredRoom] = useState(false);
  const [startedGame, setStartedGame] = useState(false);

  const onChangeRoom = (e) => {
    setRoom(e.target.value);
  };
  const onChangeUserName = (e) => {
    setUsername(e.target.value);
  };

  const onClick = () => {
    if ((room.length === 4) & (username.length !== 0)) {
      setEnteredRoom(true);
      socket.emit("join", { username: username, room: room });
    } else {
      alert("Room Code must be 4 characters");
    }
  };

  const onErase = () => {
    setEnteredRoom(false);
    setRoom("");
    setUsername("");
    socket.emit("delete_history", {});
  };

  const onStartGame = () => {
    socket.emit("start_game", room);
  };

  /**
   * socket.io - game_started
   */
  const handleStartedGame = useCallback(() => {
    setStartedGame(true);
    console.log("Does this happen")
  }, []);

  useEffect(() => {
    socket.on("game_started", handleStartedGame);

    return () => socket.off("game_started", handleStartedGame);
  }, [handleStartedGame, socket]);

  return (
    <div>
      {!enteredRoom && (
        <div className="container">
          <div className="row">
            <label>Username</label>
            <input
              value={username}
              name="username"
              onChange={(e) => onChangeUserName(e)}
            />
          </div>
          <div className="row">
            <label>Room</label>
            <input value={room} name="room" onChange={(e) => onChangeRoom(e)} />
          </div>
          <div className="row">
            <button onClick={() => onClick()}>Enter Room</button>
          </div>
        </div>
      )}

      {enteredRoom && (
        <MessageBox
          username={username}
          room={room}
          startedGame={startedGame}
          onStartGame={onStartGame}
        />
      )}
      {startedGame && <PlayingArea />}
      <button onClick={() => onErase()}>Erase</button>
    </div>
  );
};

export default Main;
