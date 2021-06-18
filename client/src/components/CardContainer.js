import Card from "./Card";
import CardUnknown from "./CardUnknown";

const CardContainer = ({ cards, sid, sids, names, turn, onCardClick }) => {
  const index = sids.indexOf(sid);
  const userCards = cards[index];
  const otherCards = cards.filter((card, i) => i !== index);

  return (
    <div className="card">
      <div className="d-flex flex-wrap justify-content-center">
        {userCards.map((card, index) => (
          <Card
            key={card.id}
            text={card.text}
            attack={card.attack}
            cost={card.cost}
            id={card.id}
            onCardClick={onCardClick}
          />
        ))}
      </div>
      <div className="d-flex flex-wrap justify-content-center">
        {otherCards.map((card) => card.map((i) => <CardUnknown key={i.id} id={""} />))}
      </div>
    </div>
  );
};

export default CardContainer;
