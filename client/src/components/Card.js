const Card = ({ text, attack, cost, id, onCardClick }) => {
  return (
    <div className="p-1">
      <div
        className="card d-flex justify-content-center align-items-center card-cursor"
        style={{ width: "8rem", height: "12rem" }}
        onClick={() => onCardClick(id)}
      >
        <div>Text: {text}</div>
        <div>Attack: {attack}</div>
        <div>Cost: {cost}</div>
        <div>ID: {id}</div>
      </div>
    </div>
  );
};

Card.defaultProps = {
  onCardClick: () => console.log("Not Valid"),
};

export default Card;
