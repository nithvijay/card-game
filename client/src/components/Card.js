const Card = ({ text, attack, cost, id }) => {
  return (
    <div className="card">
      <div>Text: {text}</div>
      <div>Attack: {attack}</div>
      <div>Cost: {cost}</div>
      <div>ID: {id}</div>
    </div>
  );
};

export default Card;
