const Scoreboard = ({ scores, userNames }) => {
  return (
    <div className="p-3">
      <div className="row">
        {scores.map((score, index) => (
          <div className="col" key={index}>
            <div className="card text-center">
              <div className="scorecard-player-name">{userNames[index]}</div>
              <div className="scorecard-player-score">{score}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Scoreboard;
