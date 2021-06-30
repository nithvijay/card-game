import Card from "./Card"

const PlayedCardsArea = ({ playedCards }) => {
  return (
    <div className="d-flex justify-content-center"
    style={{ height: "17rem"}}>
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
