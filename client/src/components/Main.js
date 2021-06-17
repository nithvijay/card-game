import { useState, useContext, useCallback, useEffect } from "react";
import { SocketContext } from "../context/socket";

import MessageBox from "./MessageBox";
import PlayingArea from "./PlayingArea";

const Main = () => {
  const socket = useContext(SocketContext);
  const [username, setUsername] = useState("Test");
  const [room, setRoom] = useState("ABCD");
  const [enteredRoom, setEnteredRoom] = useState(false);
  const [startedGame, setStartedGame] = useState(false);
  const [validatedMessage, setValidatedMessage] = useState("");
  const [validated, setValidated] = useState(true);

  const onChangeRoom = (e) => {
    setRoom(e.target.value);
  };
  const onChangeUserName = (e) => {
    setUsername(e.target.value);
  };

  const onClick = (e) => {
    e.preventDefault();
    if ((room.length === 4) & (username.length !== 0)) {
      socket.emit("join", { username: username, room: room });
    } else {
      alert("Room Code must be 4 characters");
    }
  };

  const onErase = () => {
    setEnteredRoom(false);
    setStartedGame(false);
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
  }, []);

  useEffect(() => {
    socket.on("game_started", handleStartedGame);

    return () => socket.off("game_started", handleStartedGame);
  }, [handleStartedGame, socket]);

  /**
   * socket.io - entered_room
   */
  const handleEnteredRoom = useCallback((data) => {
    if (data !== "T") {
      setValidatedMessage(data);
      setValidated(false);
    } else {
      setEnteredRoom(true);
    }
  }, []);

  useEffect(() => {
    socket.on("entered_room", handleEnteredRoom);

    return () => socket.off("entered_room", handleEnteredRoom);
  }, [handleEnteredRoom, socket]);

  return (
    <div className="container-sm" style={{ maxWidth: "100%" }}>
      {!enteredRoom && (
        <div className="card mt-5">
          <div className="card-body">
            <form onSubmit={(e) => onClick(e)}>
              <div className="row m-3 align-items-center">
                <div className="col-sm-4">
                  <label className="col-form-label fs-2">Username</label>
                </div>
                <div className="col-sm-8">
                  <input
                    className={
                      "form-control form-control-lg " +
                      (!validated && "is-invalid")
                    }
                    value={username}
                    name="username"
                    onChange={(e) => onChangeUserName(e)}
                  />
                  <span style={{ color: "red" }}>{validatedMessage}</span>
                </div>
              </div>
              <div className="row m-3 align-items-center">
                <div className="col-sm-4">
                  <label className="col-form-label fs-2">Room</label>
                </div>
                <div className="col-sm-8">
                  <input
                    className="form-control form-control-lg"
                    value={room}
                    name="room"
                    onChange={(e) => onChangeRoom(e)}
                  />
                </div>
              </div>
              <div className="row m-3">
                <button
                  className="btn btn-primary btn-lg col-md-4 offset-sm-4"
                  type="submit"
                >
                  Enter Room
                </button>
              </div>
            </form>
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

      {startedGame && <PlayingArea room={room} />}
      <button onClick={() => onErase()}>Erase</button>
    </div>
  );
};

export default Main;
