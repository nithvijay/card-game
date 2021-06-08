import Card from "./Card";

const CardContainer = ({ cards, sid, sids, names, turn }) => {
  console.log(cards);
  return (
    <div className="card-container">
      {cards.map((userCards) =>
        userCards.map((card, index) => (
          <Card
            key={index}
            text={card.text}
            attack={card.attack}
            cost={card.cost}
            id={card.id}
          />
        ))
      )[0]}
    </div>
  );
};

export default CardContainer;
