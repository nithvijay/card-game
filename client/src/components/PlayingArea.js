import { useState, useCallback, useEffect, useContext } from "react";
import { SocketContext } from "../context/socket";
import PlayedCardsArea from "./PlayedCardsArea";
import CardContainer from "./CardContainer";
import Scoreboard from "./Scoreboard";

const PlayingArea = ({ room, mainID }) => {
  const socket = useContext(SocketContext);

  const [gameState, setGameState] = useState({});
  const [userIndex, setUserIndex] = useState(0);
  const [gameLoaded, setGameLoaded] = useState(false);

  const onCardClick = (id) => {
    socket.emit("played card", { id: id, room: room });
  };

  /**
   * socket.io - gameState
   */
  const handleGameState = useCallback(
    (data) => {
      setGameState(data);
      setGameLoaded(true);
      console.log("handleGameState");
      console.log(data);
      setUserIndex(data["userMainIDs"].indexOf(mainID));
    },
    [mainID]
  );

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
            lastRoundDesc={gameState.lastRoundDesc}
            totalNumberOfRounds={gameState.totalNumberOfRounds}
          />

          <PlayedCardsArea
            playedCards={gameState.centerCards}
            mainID={mainID}
            mainIDs={gameState.userMainIDs}
            names={gameState.userNames}
            centerCardsPlayerIndex={gameState.centerCardsPlayerIndex}
          />

          <CardContainer
            cards={gameState.userCards}
            mainID={mainID}
            mainIDs={gameState.userMainIDs}
            names={gameState.userNames}
            turn={gameState.turn}
            onCardClick={onCardClick}
            level={gameState.userEnergies[userIndex]}
            maxLevel={gameState.maxEnergy}
          />
        </>
      )}
    </div>
  );
};

export default PlayingArea;
