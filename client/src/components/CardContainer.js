import Card from "./Card";
import CardUnknown from "./CardUnknown";

const CardContainer = ({ cards, sid, sids, names, turn, onCardClick }) => {
  const index = sids.indexOf(sid);
  const userCards = cards[index];
  const otherCards = cards.filter((card, i) => i !== index);

  return (
    <div className="card">
      <div className="d-flex flex-wrap">
        {userCards.map((card, index) => (
          <Card
            key={index}
            text={card.text}
            attack={card.attack}
            cost={card.cost}
            id={card.id}
            onCardClick={onCardClick}
          />
        ))}
      </div>
      <div className="d-flex flex-wrap">
        {otherCards.map((card) => card.map((i) => <CardUnknown id={""} />))}
      </div>
    </div>
  );
};

export default CardContainer;
