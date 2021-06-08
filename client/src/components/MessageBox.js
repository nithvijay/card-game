import { useState, useContext, useEffect, useCallback } from "react";
import { SocketContext } from "../context/socket";

const MessageBox = ({ username, room, startedGame, onStartGame }) => {
  const socket = useContext(SocketContext);

  const [messages, setMessages] = useState([`Hello And Welcome ${username}`]);
  const [message, setMessage] = useState("");
  const [roomMembers, setRoomMembers] = useState([]);

  /**
   * socket.io - message
   */
  const handleMessage = useCallback(
    (data) => {
      setMessages([...messages, data["message"]]);
      console.log(messages);
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
  const handleUpdateRoom = useCallback(
    (data) => {
      setRoomMembers(data["room_occupants"]);
    },
    []
  );

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

  const onClick = () => {
    if (message !== "") {
      socket.emit("message", {
        room: room,
        username: username,
        message: message,
      });
      setMessage("");
    } else {
      alert("Please Add A Message");
    }
  };

  return (
    <div className="container">
      {messages.length > 0 &&
        messages.map((msg, index) => (
          <div className="row" key={index}>
            <p>{msg}</p>
          </div>
        ))}

      <div className="row">
        <input
          value={message}
          name="message"
          onChange={(e) => onChangeMessage(e)}
        />
        <button onClick={() => onClick()}>Send Message</button>
      </div>

      <strong>People in the Room</strong>
      <ul>
        {roomMembers.map((member, index) => (
          <li key={index}>{member}</li>
        ))}
      </ul>
      {!startedGame && (
        <button onClick={() => onStartGame()}>Start Game</button>
      )}
    </div>
  );
};

export default MessageBox;
