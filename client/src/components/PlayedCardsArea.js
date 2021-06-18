import Card from "./Card"

const PlayedCardsArea = ({ playedCards }) => {
  return (
    <div>
      {playedCards.map((card, index) => (
        <Card
          key={index}
          text={card.text}
          attack={card.attack}
          cost={card.cost}
          id={card.id}
        />
      ))}
    </div>
  );
};

export default PlayedCardsArea;
