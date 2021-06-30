import { useState, useContext, useCallback, useEffect } from "react";
import { SocketContext } from "../context/socket";

const Login = ({ username, room, setUsername, setRoom, setEnteredRoom}) => {
  const socket = useContext(SocketContext);
  const [validatedMessage, setValidatedMessage] = useState("");
  const [validated, setValidated] = useState(true);

  const onChangeRoom = (e) => {
    setRoom(e.target.value);
  };
  const onChangeUserName = (e) => {
    setUsername(e.target.value);
  };

  const onFormSubmit = (e) => {
    e.preventDefault();
    if ((room.length === 4) & (username.length !== 0)) {
      socket.emit("join", { username: username, room: room });
    } else {
      alert("Room Code must be 4 characters");
    }
  };
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
  }, [setEnteredRoom]);

  useEffect(() => {
    socket.on("entered_room", handleEnteredRoom);

    return () => socket.off("entered_room", handleEnteredRoom);
  }, [handleEnteredRoom, socket]);

  return (
    <div className="card mt-5">
      <div className="card-body">
        <form onSubmit={(e) => onFormSubmit(e)}>
          <div className="row m-3 align-items-center">
            <div className="col-sm-4">
              <label className="col-form-label fs-2">Username</label>
            </div>
            <div className="col-sm-8">
              <input
                className={
                  "form-control form-control-lg " + (!validated && "is-invalid")
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
  );
};

export default Login;
