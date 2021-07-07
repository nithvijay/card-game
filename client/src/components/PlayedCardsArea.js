import Card from "./Card";
import CardUnknown from "./CardUnknown";

const PlayedCardsArea = ({
  playedCards,
  mainID,
  mainIDs,
  names,
  centerCardsPlayerIndex,
}) => {
  const playerIndex = mainIDs.indexOf(mainID);
  const playedCardsIndex = centerCardsPlayerIndex.indexOf(playerIndex);
  const playerPlayedCard =
    playedCardsIndex >= 0 ? playedCards[playedCardsIndex] : false;
  const otherCards = playedCards.filter((card, i) => i !== playedCardsIndex);
  const namesFiltered = names.filter((name, i) => i !== playedCardsIndex);

  return (
    <div className="d-flex justify-content-center" style={{ height: "14.5rem" }}>
      {/* indicates that the user has played a card for that turn */}
      {playerPlayedCard && (
        <div className="d-flex flex-column align-items-center">
          <Card
            text={playerPlayedCard.text}
            attack={playerPlayedCard.attack}
            cost={playerPlayedCard.cost}
            id={playerPlayedCard.id}
          />
          <div>{names[playerIndex]}</div>
        </div>
      )}

      {otherCards.map((card, index) => (
        <div key={index} className="d-flex flex-column align-items-center">
          <CardUnknown
            text={card.text}
            attack={card.attack}
            cost={card.cost}
            id={card.id}
          />
          <div>{namesFiltered[centerCardsPlayerIndex[index]]}</div>
        </div>
      ))}
    </div>
  );
};

export default PlayedCardsArea;
