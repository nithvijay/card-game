const Scoreboard = ({ scores, userNames }) => {
  return (
    <div className="p-3">
      <div className="card">
        <div className="container">
          {scores.map((score, index) => (
            <div key={index}>
              {score} - {userNames[index]}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Scoreboard;
