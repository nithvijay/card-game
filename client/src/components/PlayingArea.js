import { useState, useCallback, useEffect, useContext } from "react";
import { SocketContext } from "../context/socket";
import PlayedCardsArea from "./PlayedCardsArea";
import CardContainer from "./CardContainer";

const PlayingArea = () => {
  const socket = useContext(SocketContext);
  const socketID = socket.id;
  const [cardsInHand, setCards] = useState({
    cards: ["Sword", "Gun", "Knife", "Fist"],
  });

  const [gameState, setGameState] = useState({});
  const [gameLoaded, setGameLoaded] = useState(false);

  /**
   * socket.io - gameState
   */
  const handleGameState = useCallback((data) => {
    setGameState(data);
    console.log(data);
    setGameLoaded(true);
  }, []);

  useEffect(() => {
    socket.on("update_game_state", handleGameState);

    return () => socket.off("update_game_state", handleGameState);
  }, [handleGameState, socket]);

  return (
    <div>
      {gameLoaded && (
        <div className="playing-container">
          <PlayedCardsArea playedCards={gameState.centerCards} />

          <CardContainer
            cards={gameState.userCards}
            sid={socketID}
            sids={gameState.userSIDs}
            names={gameState.userNames}
            turn={gameState.turn}
          />
        </div>
      )}
    </div>
  );
};

export default PlayingArea;
