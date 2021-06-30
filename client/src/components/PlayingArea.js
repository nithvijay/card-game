import { useState, useCallback, useEffect, useContext } from "react";
import { SocketContext } from "../context/socket";
import PlayedCardsArea from "./PlayedCardsArea";
import CardContainer from "./CardContainer";
import Scoreboard from "./Scoreboard";
import EnergyBar from "./EnergyBar";

const PlayingArea = ({ room }) => {
  const socket = useContext(SocketContext);
  const socketID = socket.id;

  const [gameState, setGameState] = useState({});
  const [userIndex, setUserIndex] = useState(0);
  const [gameLoaded, setGameLoaded] = useState(false);

  const onCardClick = (id) => {
    socket.emit("played card", { id: id, room: room });
  };

  /**
   * socket.io - gameState
   */
  const handleGameState = useCallback((data) => {
    setGameState(data);
    setGameLoaded(true);
    console.log("handleGameState");
    console.log(data);
    setUserIndex(data['userSIDs'].indexOf(socketID));
  }, [socketID]);

  useEffect(() => {
    socket.on("update_game_state", handleGameState);

    return () => socket.off("update_game_state", handleGameState);
  }, [handleGameState, socket]);

  return (
    <div className="card mt-2 p-3">
      {gameLoaded && (
        <>
          <Scoreboard
            userNames={gameState.userNames}
            scores={gameState.scores}
          />

          <PlayedCardsArea playedCards={gameState.centerCards} />

          <EnergyBar level={gameState.userEnergies[userIndex]} maxLevel={gameState.maxEnergy} />

          <CardContainer
            cards={gameState.userCards}
            sid={socketID}
            sids={gameState.userSIDs}
            names={gameState.userNames}
            turn={gameState.turn}
            onCardClick={onCardClick}
          />
        </>
      )}
    </div>
  );
};

export default PlayingArea;
