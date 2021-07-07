import Card from "./Card";
import CardUnknown from "./CardUnknown";
import EnergyBar from "./EnergyBar";

const CardContainer = ({
  cards,
  mainID,
  mainIDs,
  names,
  turn,
  onCardClick,
  level,
  maxLevel,
}) => {
  const index = mainIDs.indexOf(mainID);
  const userCards = cards[index];
  const otherCards = cards.filter((card, i) => i !== index);
  const filteredNames = names.filter((name, i) => i !== index);

  return (
    <div className="d-flex flex-wrap flex-row justify-content-center">
      <div
        className="d-flex card flex-column p-2"
        style={{ borderLeft: "5px solid grey" }}
      >
        <div className="p-2" style={{ backgroundColor: "#f2f2f2" }}>
          {names[index]}
        </div>
        <div className="align-items-center">
          <div className="col">
            <div className="d-flex flex-wrap justify-content-center mt-3">
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
            <EnergyBar level={level} maxLevel={maxLevel} />
          </div>
        </div>
      </div>

      {otherCards.map((otherUserCards, index) => (
        <div
          key={filteredNames[index]}
          className="d-flex card flex-column p-2"
          style={{ borderLeft: "5px solid silver" }}
        >
          <div className="p-2" style={{ backgroundColor: "#f2f2f2" }}>
            {filteredNames[index]}
          </div>
          <div className="align-items-center">
            <div className="col">
              <div className="d-flex flex-wrap justify-content-center mt-3">
                {otherUserCards.map((card) => (
                  <div key={card.id}>
                    <CardUnknown id={card.id} />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default CardContainer;
