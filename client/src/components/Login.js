import { useState, useContext, useCallback, useEffect } from "react";
import { SocketContext } from "../context/socket";

const Login = ({ username, room, setUsername, setRoom, setEnteredRoom }) => {
  const socket = useContext(SocketContext);
  const [validatedUsernameMessage, setValidatedUsernameMessage] = useState("");
  const [isUsernameValidated, setIsUsernameValidated] = useState(true);
  const [validatedRoomMessage, setValidatedRoomMessage] = useState("");
  const [isRoomValidated, setIsRoomValidated] = useState(true);

  const onChangeRoom = (e) => {
    setRoom(e.target.value.toUpperCase());
    if (!isRoomValidated) {
      setValidatedRoomMessage("");
      setIsRoomValidated(true);
    }
  };
  const onChangeUserName = (e) => {
    setUsername(e.target.value);
    if (!isUsernameValidated) {
      setValidatedUsernameMessage("");
      setIsUsernameValidated(true);
    }
  };

  const onFormSubmit = (e) => {
    e.preventDefault();
    if (room.length !== 4) {
      setValidatedRoomMessage("Room must be 4 characters");
      setIsRoomValidated(false);
    } else if (username.length === 0) {
      setValidatedUsernameMessage("Please input a username");
      setIsUsernameValidated(false);
    } else {
      socket.emit("join", { username: username, room: room });
    }
  };
  /**
   * socket.io - entered_room
   */
  const handleEnteredRoom = useCallback(
    (data) => {
      if (data !== "T") {
        if (data.startsWith("Game")) {
          setValidatedRoomMessage(data);
          setIsRoomValidated(false);
        } else if (data.startsWith("Username")) {
          setValidatedUsernameMessage(data);
          setIsUsernameValidated(false);
        }
      } else {
        setIsUsernameValidated(true);
        setIsRoomValidated(true);
        setEnteredRoom(true);
      }
    },
    [setEnteredRoom]
  );

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
                  "form-control form-control-lg " +
                  (!isUsernameValidated && "is-invalid")
                }
                value={username}
                name="username"
                onChange={(e) => onChangeUserName(e)}
              />
              <span style={{ color: "red" }}>
                &nbsp;
                {validatedUsernameMessage}
              </span>
            </div>
          </div>
          <div className="row m-3 align-items-center">
            <div className="col-sm-4">
              <label className="col-form-label fs-2">Room</label>
            </div>
            <div className="col-sm-8">
              <input
                className={
                  "form-control form-control-lg " +
                  (!isRoomValidated && "is-invalid")
                }
                value={room}
                name="room"
                onChange={(e) => onChangeRoom(e)}
              />
              <div style={{ color: "red" }}>
                &nbsp;
                {validatedRoomMessage}
              </div>
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
