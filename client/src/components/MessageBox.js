import { useState, useContext, useEffect, useCallback, useRef } from "react";
import { SocketContext } from "../context/socket";

const MessageBox = ({ username, room, startedGame, onStartGame }) => {
  const socket = useContext(SocketContext);

  const [messages, setMessages] = useState([`Hello And Welcome ${username}`]);
  const [message, setMessage] = useState("");
  const [roomMembers, setRoomMembers] = useState([]);
  const divRef = useRef(null);

  useEffect(() => {
    divRef.current.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  /**
   * socket.io - message
   */
  const handleMessage = useCallback(
    (data) => {
      setMessages([...messages, data["message"]]);
    },
    [messages]
  );

  useEffect(() => {
    socket.on("message", handleMessage);

    return () => socket.off("message", handleMessage);
  }, [handleMessage, socket]);

  /**
   * socket.io - update_room_members
   */
  const handleUpdateRoom = useCallback((data) => {
    setRoomMembers(data["room_occupants"]);
  }, []);

  useEffect(() => {
    socket.on("update_room_members", handleUpdateRoom);

    return () => socket.off("update_room_members", handleUpdateRoom);
  }, [handleUpdateRoom, socket]);

  /**
   * socket.io - message_history
   */
  const handleMessageHistory = useCallback((data) => {
    setMessages(data["message_history"]);
  }, []);

  useEffect(() => {
    socket.on("message_history", handleMessageHistory);

    return () => socket.off("message_history", handleMessageHistory);
  }, [handleMessageHistory, socket]);

  /**
   *  Other stuff
   */
  const onChangeMessage = (e) => {
    setMessage(e.target.value);
  };

  const onFormSubmit = (e) => {
    e.preventDefault();
    if (message !== "") {
      socket.emit("message", {
        room: room,
        username: username,
        message: message,
      });
      setMessage("");
    }
  };

  return (
    <div className="card mt-5">
      <div className="row p-3">
        <div className="col-sm-9">
          <div className="card p-3">
            <div className="overflow-scroll" style={{ height: "36vh" }}>
              {messages.length > 0 &&
                messages.map((msg, index) => <p key={index}>{msg}</p>)}
              <div ref={divRef} />
            </div>

            <form className="input-group" onSubmit={(e) => onFormSubmit(e)}>
              <input
                className="form-control"
                value={message}
                name="message"
                onChange={(e) => onChangeMessage(e)}
              />
              <button className="btn btn-outline-secondary" type="submit">
                Send Message
              </button>
            </form>
          </div>
        </div>
        <div className="col-sm-3">
          <div className="card">
            <div className="card-header">People in the Room</div>
            <div className="card-body">
              <ul>
                {roomMembers.map((member, index) => (
                  <li key={index}>{member}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {!startedGame && (
        <button className="btn btn-primary" onClick={() => onStartGame()}>
          Start Game
        </button>
      )}
    </div>
  );
};

export default MessageBox;
