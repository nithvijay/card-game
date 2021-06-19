import { useState, useContext, useCallback, useEffect } from "react";
import { SocketContext } from "../context/socket";

import Login from "./Login";
import MessageBox from "./MessageBox";
import PlayingArea from "./PlayingArea";

const Main = () => {
  const socket = useContext(SocketContext);
  const [username, setUsername] = useState("Test");
  const [room, setRoom] = useState("ABCD");
  const [enteredRoom, setEnteredRoom] = useState(false);
  const [startedGame, setStartedGame] = useState(false);
  const [gameWinner, setGameWinner] = useState("");

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
   * socket.io - win_game
   */
  const handleWinGame = useCallback((data) => {
    setStartedGame(false);
    setGameWinner(data);
  }, []);

  useEffect(() => {
    socket.on("win_game", handleWinGame);

    return () => socket.off("win_game", handleWinGame);
  }, [handleWinGame, socket]);

  return (
    <div className="container-sm" style={{ maxWidth: "100%" }}>
      {!enteredRoom && (
        <Login
          username={username}
          setUsername={setUsername}
          room={room}
          setRoom={setRoom}
          setEnteredRoom={setEnteredRoom}
        />
      )}

      {enteredRoom && (
        <MessageBox
          username={username}
          room={room}
          startedGame={startedGame}
          onStartGame={onStartGame}
        />
      )}

      {gameWinner.length > 0 && (
        <div className="card p-2 m-2">{gameWinner} won!</div>
      )}

      {startedGame && <PlayingArea room={room} />}
      <button onClick={() => onErase()}>Erase</button>
    </div>
  );
};

export default Main;
